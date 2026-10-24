import json,pathlib,secrets,time,threading,socket,ipaddress,re,hashlib
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
import learning_companion as learning
ROOT=pathlib.Path(__file__).resolve().parent;DATA=ROOT/'data'
SERVER=None;SESSIONS={};FAILURES={};LOCK=threading.Lock();PIN='';ADDRESS='';PORT=18766
def reply(handler,body,status=200,headers=None):
 raw=json.dumps(body,ensure_ascii=False).encode();handler.send_response(status);handler.send_header('Content-Type','application/json; charset=utf-8');handler.send_header('Content-Length',str(len(raw)));handler.send_header('Cache-Control','no-store')
 for k,v in (headers or {}).items():handler.send_header(k,v)
 handler.end_headers();handler.wfile.write(raw)
def authenticated(handler):
 cookies=dict(re.findall(r'(?:^|;\s*)([^=;]+)=([^;]+)',handler.headers.get('Cookie','')));key=cookies.get('study_pair','')
 with LOCK:return bool(SESSIONS.get(hashlib.sha256(key.encode()).hexdigest(),0)>time.time())
class MobileHandler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def check_host(self):return self.headers.get('Host','') in {ADDRESS+':'+str(PORT),'127.0.0.1:'+str(PORT),'localhost:'+str(PORT)}
 def send_file(self,file,mime):
  raw=file.read_bytes();self.send_response(200);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(raw)
 def do_GET(self):
  try:
   if not self.check_host():return reply(self,{'error':'Host denied'},403)
   path=self.path.split('?')[0]
   if path in ['/','/mobile']:return self.send_file(ROOT/'mobile.html','text/html; charset=utf-8')
   static={'/mobile.js':'text/javascript; charset=utf-8','/mobile.css':'text/css; charset=utf-8','/problem_workspace.js':'text/javascript; charset=utf-8'}
   if path in static:return self.send_file(ROOT/path[1:],static[path])
   if not authenticated(self):return reply(self,{'error':'请先用电脑显示的配对码连接。'},401)
   if path=='/api/exercise-pdf':
    import exercise_pdf
    raw=exercise_pdf.packet();self.send_response(200);self.send_header('Content-Type','application/pdf');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw);return
   if path=='/api/learning/export':return reply(self,learning.export_backup())
   if path=='/api/learning':return reply(self,learning.snapshot())
   if path=='/api/problem-questions':return reply(self,[learning.public_question(q) for q in learning.QUESTIONS])
   if path.startswith('/api/mistake-image/'):
    name=path.rsplit('/',1)[-1]
    if not re.fullmatch(r'[a-f0-9]{32}\.(?:jpg|pdf)',name):raise ValueError('图片名无效')
    return self.send_file(DATA/'mistake-images'/name,'application/pdf' if name.endswith('.pdf') else 'image/jpeg')
   return reply(self,{'error':'未知页面'},404)
  except Exception as e:return reply(self,{'error':str(e)},400)
 def do_POST(self):
  try:
   if not self.check_host():return reply(self,{'error':'Host denied'},403)
   expected='http://'+self.headers['Host']
   if self.headers.get('Origin') not in [expected,None]:return reply(self,{'error':'Origin denied'},403)
   length=int(self.headers.get('Content-Length',0))
   if not 0<length<=12500000:raise ValueError('请求太大或为空')
   body=json.loads(self.rfile.read(length));path=self.path
   if path=='/api/pair':
    ip=self.client_address[0]
    with LOCK:
     failures=[t for t in FAILURES.get(ip,[]) if time.time()-t<900]
     if len(failures)>=8:return reply(self,{'error':'配对尝试过多，15分钟后再试。'},429)
     if not secrets.compare_digest(str(body.get('pin','')),PIN):FAILURES[ip]=failures+[time.time()];return reply(self,{'error':'配对码不正确。'},403)
     session=secrets.token_urlsafe(32);SESSIONS[hashlib.sha256(session.encode()).hexdigest()]=time.time()+30*86400;FAILURES.pop(ip,None);(DATA/'mobile-sessions.json').write_text(json.dumps(SESSIONS),encoding='utf-8')
    return reply(self,{'paired':True},headers={'Set-Cookie':'study_pair='+session+'; HttpOnly; SameSite=Strict; Path=/; Max-Age=2592000'})
   if not authenticated(self):return reply(self,{'error':'请先配对。'},401)
   routes={'/api/learning/grade':learning.grade,'/api/learning/mistake':learning.save_mistake,'/api/learning/drawing':learning.save_drawing,'/api/learning/score':learning.save_score,'/api/learning/correction':learning.update_mistake,'/api/learning/reference':learning.reference_check}
   if path not in routes:return reply(self,{'error':'移动端不提供此操作'},403)
   return reply(self,routes[path](body))
  except Exception as e:return reply(self,{'error':str(e)},400)
def start():
 global SERVER,PIN,ADDRESS
 if SERVER:return info()
 configPath=DATA/'mobile-access.json'
 if configPath.exists():config=json.loads(configPath.read_text(encoding='utf-8'))
 else:config={'pin':str(secrets.randbelow(90000000)+10000000),'address':'192.168.16.110'};configPath.write_text(json.dumps(config),encoding='utf-8')
 PIN=config['pin'];sessionPath=DATA/'mobile-sessions.json'
 if sessionPath.exists():SESSIONS.update({k:v for k,v in json.loads(sessionPath.read_text()).items() if re.fullmatch(r'[a-f0-9]{64}',k) and float(v)>time.time()})
 addresses=socket.gethostbyname_ex(socket.gethostname())[2]
 ADDRESS=config.get('address') if config.get('address') in addresses else next((a for a in addresses if a.startswith('192.168.')), '')
 if not ADDRESS:return {'available':False,'message':'尚未发现Wi-Fi局域网地址。'}
 SERVER=ThreadingHTTPServer((ADDRESS,PORT),MobileHandler);threading.Thread(target=SERVER.serve_forever,daemon=True).start();return info()
def info():return {'available':bool(SERVER),'url':'http://'+ADDRESS+':'+str(PORT)+'/mobile' if ADDRESS else '', 'pin':PIN,'message':'手机／平板与电脑连接同一Wi-Fi，输入配对码。电脑工作台需保持运行。'}
def close():
 global SERVER
 if SERVER:SERVER.shutdown();SERVER.server_close();SERVER=None
 return info()
