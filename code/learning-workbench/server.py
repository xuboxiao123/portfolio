import os,sys,json,pathlib,secrets,time,threading,subprocess,sqlite3,urllib.request,urllib.parse,mimetypes,zipfile,re,shutil,hashlib,io,base64
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor
from snippets import prepare
import learning_companion
import companion_server
import lesson_sessions
import transcript_store
import supplementary_store
from contextlib import contextmanager
ROOT=pathlib.Path(__file__).resolve().parent
DATA=ROOT/'data';DATA.mkdir(exist_ok=True)
RUNS=DATA/'runs';RUNS.mkdir(exist_ok=True)
CONFIG=json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
MODEL=json.loads((ROOT/'model.json').read_text(encoding='utf-8'))
PRACTICES=json.loads((ROOT/'programming_practice.json').read_text(encoding='utf-8'))
LIBRARY=json.loads((ROOT/'library.json').read_text(encoding='utf-8'))
LIB={x['id']:x for x in LIBRARY}
INDEX={}
for x in LIBRARY:
 p=DATA/'library-text'/(x['id']+'.txt')
 if p.exists():INDEX[x['id']]=p.read_text(encoding='utf-8',errors='replace')
TOKEN=secrets.token_urlsafe(32);JOBS={};LOCK=threading.Lock();POOL=ThreadPoolExecutor(max_workers=2);JAVA=None
PORT=int(sys.argv[1]) if len(sys.argv)>1 else 18765
BASE='http://127.0.0.1:'+str(PORT)
DB=DATA/'product.sqlite'
@contextmanager
def db():
 con=sqlite3.connect(DB,timeout=8);con.execute('CREATE TABLE IF NOT EXISTS telemetry(id INTEGER PRIMARY KEY, temperature REAL, command TEXT, created REAL)');con.execute('CREATE TABLE IF NOT EXISTS decisions(id INTEGER PRIMARY KEY, stage TEXT, decision TEXT, evidence TEXT, created REAL)');con.execute('CREATE TABLE IF NOT EXISTS lecture_notes(id TEXT PRIMARY KEY,title TEXT,course TEXT,week TEXT,body TEXT,updated REAL)')
 try:
  yield con;con.commit()
 except Exception:con.rollback();raise
 finally:con.close()
with db() as con:
 if not con.execute('SELECT COUNT(*) FROM telemetry').fetchone()[0]:con.execute('INSERT INTO telemetry(temperature,command,created) VALUES(?,?,?)',(26.5,'off',time.time()))
def runtime_status():
 return {k:{'available':bool(v and pathlib.Path(v).exists()),'path':v} for k,v in CONFIG.items() if k in ['python','java','javac','zig','php','vscode','arduino','arduino_cli','android','figma']}
def kill(p):
 if p.poll() is None:
  if os.name=='nt':subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
  else:p.kill()
def command(args,cwd,stdin='',timeout=20):
 out=cwd/'output.log';t=time.monotonic()
 with out.open('wb') as log:
  p=subprocess.Popen([str(a) for a in args],cwd=cwd,stdin=subprocess.PIPE,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONIOENCODING':'utf-8','MPLBACKEND':'Agg','ZIG_LOCAL_CACHE_DIR':str(DATA/'zig-cache'),'ZIG_GLOBAL_CACHE_DIR':str(DATA/'zig-global')},creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
  try:p.stdin.write(stdin.encode('utf-8'));p.stdin.close()
  except BrokenPipeError:pass
  reason=''
  while p.poll() is None:
   if time.monotonic()-t>timeout:reason='运行超过 '+str(timeout)+' 秒，已停止';kill(p);break
   if out.stat().st_size>512000:reason='输出过多，已停止';kill(p);break
   time.sleep(.1)
  p.wait(timeout=5)
 text=out.read_bytes()[:512000].decode('utf-8',errors='replace')
 return {'output':text+('\n'+reason if reason else ''),'exitCode':p.returncode,'seconds':round(time.monotonic()-t,2)}
def job(body):
 ident=secrets.token_hex(8);JOBS[ident]={'state':'running'}
 def run():
  cwd=RUNS/ident;cwd.mkdir()
  try:
   language=body.get('language','Python');source=body.get('source','');stdin=body.get('stdin','')
   if not isinstance(source,str) or len(source)>200000 or len(stdin)>100000:raise ValueError('代码或输入过长')
   for name,content in body.get('fixtures',{}).items():
    if not re.fullmatch(r'[A-Za-z0-9_.-]{1,80}',name):raise ValueError('文件名无效')
    (cwd/name).write_text(str(content)[:100000],encoding='utf-8')
   if language=='Python':
    cells=body.get('cells',[source]);assert isinstance(cells,list) and 0<len(cells)<=400 and all(isinstance(s,str) and len(s)<200000 for s in cells)
    (cwd/'cells.json').write_text(json.dumps({'cells':cells},ensure_ascii=False),encoding='utf-8')
    result=command([CONFIG['python'],'-u',ROOT/'python_cells.py',cwd/'cells.json'],cwd,stdin)
   elif language=='Java':
    (cwd/'Main.java').write_text(source,encoding='utf-8');compiled=command([CONFIG['javac'],'-encoding','UTF-8','Main.java'],cwd,timeout=40)
    result=compiled if compiled['exitCode'] else command([CONFIG['java'],'-Dfile.encoding=UTF-8','-cp',cwd,'Main'],cwd,stdin)
   elif language in ['C','C++']:
    stripped=re.sub(r'/\*.*?\*/|//[^\n]*','',source,flags=re.S)
    if not re.search(r'\bmain\s*\(',stripped):raise ValueError('这段代码只有函数或语句，缺少main入口。请从知识卡重新打开完整例题，或在代码中添加main函数并调用它。')
    ext='c' if language=='C' else 'cpp';p=cwd/('main.'+ext);p.write_text(source,encoding='utf-8')
    companions=sorted(f for f in cwd.glob('*.'+ext) if f!=p)
    compiled=command([CONFIG['zig'],'cc' if language=='C' else 'c++','-std=c11' if language=='C' else '-std=c++17','-Wall','-Wextra',p,*companions,'-o',cwd/'main.exe'],cwd,timeout=100)
    result=compiled if compiled['exitCode'] else command([cwd/'main.exe'],cwd,stdin)
   elif language=='PHP':
    (cwd/'main.php').write_text(source,encoding='utf-8');result=command([CONFIG['php'],'-n',cwd/'main.php'],cwd,stdin)
   elif language=='Arduino':
    fqbn=body.get('board','arduino:avr:uno')
    if fqbn not in ['arduino:avr:uno','esp32:esp32:esp32']:raise ValueError('请选择UNO或ESP32')
    sketch=cwd/'StudySketch';sketch.mkdir();(sketch/'StudySketch.ino').write_text(source,encoding='utf-8')
    result=command([CONFIG['arduino_cli'],'compile','--jobs','4','--fqbn',fqbn,'--build-path',cwd/'build',sketch],cwd,timeout=300)
    result['output']+='\n仅编译，没有上传硬件。'
   else:raise ValueError('不支持的运行语言')
   result.update(state='done',plots=['/runs/'+ident+'/'+p.name for p in cwd.glob('plot-*.png')]);JOBS[ident]=result
  except Exception as e:JOBS[ident]={'state':'done','output':type(e).__name__+': '+str(e),'exitCode':1,'plots':[]}
 POOL.submit(run);return ident
def project_folder():
 p=ROOT/'projects/智能桌面助手';p.mkdir(parents=True,exist_ok=True);return p
def open_editor(body):
 language=body.get('language','Python');text=body.get('source','')
 ext={'Python':'py','Java':'java','C':'c','C++':'cpp','PHP':'php','HTML':'html','Arduino':'ino'}.get(language)
 if not ext or not isinstance(text,str) or len(text)>200000:raise ValueError('无效源文件')
 p=DATA/'我的实验'/('experiment-'+secrets.token_hex(4));p.mkdir(parents=True,exist_ok=True)
 for name,content in body.get('fixtures',{}).items():
  if not re.fullmatch(r'[A-Za-z0-9_.-]{1,80}',name):raise ValueError('附属文件名无效')
  (p/name).write_text(str(content)[:100000],encoding='utf-8')
 if language=='Arduino':p=p/'StudySketch';p.mkdir(exist_ok=True);name='StudySketch.ino'
 else:name='Main.java' if language=='Java' else 'study.'+ext
 target=p/name;target.write_text(text,encoding='utf-8')
 tool=body.get('tool','vscode')
 if tool=='powershell':
  def q(s):return "'"+str(s).replace("'","''")+"'"
  if language not in ['C','C++','Java','PHP','Python']:raise ValueError('此语言使用编辑器或网页预览')
  if language in ['C','C++']:
   companions=sorted(f for f in p.glob('*.'+ext) if f!=target)
   cmd='& '+q(CONFIG['zig'])+(' cc -std=c11 ' if language=='C' else ' c++ -std=c++17 ')+' '.join(q(f) for f in [target,*companions])+' -o '+q(p/'study.exe')+'; if ($LASTEXITCODE -eq 0) { & '+q(p/'study.exe')+' }'
  elif language=='Java':cmd='& '+q(CONFIG['javac'])+' -encoding UTF-8 '+q(target)+'; if ($LASTEXITCODE -eq 0) { & '+q(CONFIG['java'])+' -cp '+q(p)+' Main }'
  else:cmd='& '+q(CONFIG['php' if language=='PHP' else 'python'])+' '+q(target)
  subprocess.Popen(['powershell.exe','-NoLogo','-NoExit','-Command',cmd],cwd=p,creationflags=subprocess.CREATE_NEW_CONSOLE)
 else:
  exe=CONFIG.get('arduino') if tool=='arduino' else CONFIG.get('vscode')
  if not exe or not pathlib.Path(exe).exists():raise ValueError('尚未找到对应编辑器')
  subprocess.Popen([exe,str(p),str(target)] if tool=='vscode' else [exe,str(target)],cwd=p,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 return {'path':str(target),'message':'已保存实验副本并打开'+('PowerShell' if tool=='powershell' else 'Arduino IDE' if tool=='arduino' else 'VS Code')}
def start_java():
 global JAVA
 if JAVA and JAVA.poll() is None:return {'message':'Java后端已经运行','port':18867}
 folder=project_folder()/'java-backend';compiled=command([CONFIG['javac'],'-encoding','UTF-8',folder/'Main.java'],folder,timeout=40)
 if compiled['exitCode']:raise ValueError(compiled['output'])
 JAVA=subprocess.Popen([CONFIG['java'],'-Dfile.encoding=UTF-8','-cp',folder,'Main'],cwd=folder,stdout=(DATA/'java-server.log').open('ab'),stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
 for _ in range(30):
  try:
   with urllib.request.urlopen('http://127.0.0.1:18867/data',timeout=.5) as r:payload=json.load(r)
   if payload.get('service')=='study-java':return {'message':'Java HTTP后端已启动','port':18867}
  except Exception:time.sleep(.1)
 kill(JAVA);raise ValueError('Java后端启动失败，查看运行日志')
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def reply(self,obj,status=200):self.send(json.dumps(obj,ensure_ascii=False).encode(),'application/json; charset=utf-8',status)
 def send(self,content,kind,status=200):
  self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(content)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('X-Frame-Options','SAMEORIGIN');self.end_headers();self.wfile.write(content)
 def host_ok(self):return self.headers.get('Host') in ['127.0.0.1:'+str(PORT),'localhost:'+str(PORT),'study.localhost:'+str(PORT)]
 def send_file(self,file,kind,attachment=False):
  size=file.stat().st_size;start=0;end=size-1;partial=False
  if self.headers.get('Range'):
   match=re.fullmatch(r'bytes=(\d*)-(\d*)',self.headers['Range'])
   if not match or not any(match.groups()):return self.reply({'error':'无效范围'},416)
   if match[1]:start=int(match[1]);end=min(int(match[2]) if match[2] else end,end)
   else:start=max(0,size-int(match[2]))
   if start>end or start>=size:return self.reply({'error':'范围超出文件'},416)
   partial=True
  self.send_response(206 if partial else 200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(max(0,end-start+1)));self.send_header('Accept-Ranges','bytes');self.send_header('X-Content-Type-Options','nosniff')
  if partial:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
  if attachment:self.send_header('Content-Disposition',"attachment; filename*=UTF-8''"+urllib.parse.quote(file.name))
  self.end_headers()
  try:
   with file.open('rb') as stream:
    stream.seek(start);remaining=end-start+1
    while remaining>0:
     chunk=stream.read(min(65536,remaining))
     if not chunk:break
     self.wfile.write(chunk);remaining-=len(chunk)
  except (BrokenPipeError,ConnectionResetError):pass
 def do_GET(self):
  if not self.host_ok():return self.reply({'error':'Host denied'},403)
  path=urllib.parse.urlsplit(self.path).path
  try:
   if path=='/api/supplementary-index':return self.reply(supplementary_store.public_index())
   if path.startswith('/api/supplementary-preview/'):
    return self.reply(supplementary_store.preview(path.rsplit('/',1)[-1]))
   if path.startswith('/supplementary-file/'):
    row,file=supplementary_store.file(path.rsplit('/',1)[-1])
    kind={'.pdf':'application/pdf','.mp4':'video/mp4','.mov':'video/quicktime','.m4v':'video/mp4','.webm':'video/webm','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.gif':'image/gif','.webp':'image/webp'}.get(row['ext'],'application/octet-stream')
    attachment='download' in urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
    return self.send_file(file,kind,attachment or row['kind'] not in ['video','pdf','image'])
   if path.startswith('/api/lesson-plot/'):
    pieces=path.split('/')
    if len(pieces)!=5 or not re.fullmatch(r'[A-Za-z0-9_-]{1,90}',pieces[3]) or not re.fullmatch(r'plot-[a-f0-9]{32}\.png',pieces[4]):return self.reply({'error':'Invalid plot'},400)
    return self.send_file(DATA/'kernels'/pieces[3]/pieces[4],'image/png')
   if path=='/api/transcript':
    video=urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query).get('video',[''])[0]
    for file in (DATA/'transcripts').glob('*.json'):
     transcript=json.loads(file.read_text(encoding='utf-8'))
     if transcript.get('video')==video:return self.reply(transcript)
    return self.reply({'cues':[],'complete':False,'message':'这节录播尚未导入逐字稿；不显示其他课节的翻译。'})
   if path=='/api/exercise-pdf':
    import exercise_pdf
    return self.send(exercise_pdf.packet(),'application/pdf')
   if path=='/api/mobile-info':return self.reply(companion_server.info())
   if path=='/api/learning/export':return self.reply(learning_companion.export_backup())
   if path=='/api/learning':return self.reply(learning_companion.snapshot())
   if path=='/api/problem-questions':return self.reply([learning_companion.public_question(q) for q in learning_companion.QUESTIONS])
   if path.startswith('/api/mistake-image/'):
    name=path.rsplit('/',1)[-1]
    if not re.fullmatch(r'[a-f0-9]{32}\.(?:jpg|pdf)',name):raise ValueError('无效图片')
    return self.send_file(DATA/'mistake-images'/name,'application/pdf' if name.endswith('.pdf') else 'image/jpeg')
   if path=='/companion':return self.send((ROOT/'mobile.html').read_text(encoding='utf-8').replace('__MOBILE_TOKEN__',TOKEN).encode(),'text/html; charset=utf-8')
   if path=='/api/study-plan':return self.reply(json.loads((ROOT/'study_plan.json').read_text(encoding='utf-8')))
   if path=='/api/system-courses':
    catalog=(ROOT.parent/'系统'/'catalog.json').read_bytes()
    if 'download' in urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query):
     self.send_response(200);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Disposition','attachment; filename=UNSW-system-courses.json');self.send_header('Content-Length',str(len(catalog)));self.end_headers();self.wfile.write(catalog);return
    return self.send(catalog,'application/json; charset=utf-8')
   if path=='/api/course-index':return self.reply(json.loads((ROOT/'course_index.json').read_text(encoding='utf-8')))
   if path=='/api/lectures':return self.reply(json.loads((ROOT/'lecture_index.json').read_text(encoding='utf-8')))
   if path=='/api/health':return self.reply({'app':'fullstack-study-v1','port':PORT})
   if path=='/api/model':return self.reply(MODEL)
   if path=='/api/practices':return self.reply(PRACTICES)
   if path=='/api/knowledge-data':
    p=DATA/'knowledge.json';return self.reply(json.loads((p if p.exists() else ROOT.parent/'学习知识库数据.json').read_text(encoding='utf-8')))
   if path=='/api/notes':
    with db() as con:rows=con.execute('SELECT id,title,course,week,body,updated FROM lecture_notes WHERE body<>\'\' ORDER BY updated DESC').fetchall()
    return self.reply([dict(zip(['id','title','course','week','body','updated'],r)) for r in rows])
   if path=='/api/library':
    query=urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query).get('q',[''])[0].lower()[:150]
    rows=LIBRARY if not query else [x for x in LIBRARY if query in (x['name']+' '+x['relative']+' '+' '.join(x.get('tags',[]))+' '+INDEX.get(x['id'],'')).lower()]
    return self.reply([{**{k:v for k,v in x.items() if k not in ['path','archive']},'archive':bool(x.get('archive'))} for x in rows])
   if path=='/api/runtime':return self.reply(runtime_status())
   if path.startswith('/api/jobs/'):return self.reply(JOBS.get(path.rsplit('/',1)[-1],{'state':'missing'}))
   if path=='/api/state':
    p=DATA/'study-state.json';return self.reply(json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'progress':{},'notes':{},'notebooks':{}})
   if path=='/api/product':
    with db() as con:rows=con.execute('SELECT temperature,command,created FROM telemetry ORDER BY id DESC LIMIT 20').fetchall()
    j=None
    if JAVA and JAVA.poll() is None:
     try:
      with urllib.request.urlopen('http://127.0.0.1:18867/data',timeout=1) as r:j=json.load(r)
     except Exception:pass
    return self.reply({'mode':'模拟设备数据','samples':[{'temperature':r[0],'command':r[1],'time':r[2]} for r in rows], 'java':j})
   if path.startswith('/source/'):
    row=LIB[path.rsplit('/',1)[-1]]
    if row.get('archive'):
     with zipfile.ZipFile(row['archive']) as z:content=z.read(row['member'])
     return self.send(content,'text/plain; charset=utf-8')
    kind={'.pdf':'application/pdf','.mp4':'video/mp4','.mp3':'audio/mpeg','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg'}.get(row['type'])
    if kind:return self.send_file(pathlib.Path(row['path']),kind)
    if row['type'] not in ['.py','.java','.c','.h','.cpp','.ino','.html','.htm','.php','.css','.js','.json','.txt','.md','.sql','.csv','.xml']:
     return self.send_file(pathlib.Path(row['path']),'application/octet-stream',True)
    return self.send_file(pathlib.Path(row['path']),'text/plain; charset=utf-8')
   if path.startswith('/runs/'):
    f=(DATA/path.lstrip('/')).resolve()
    if not f.is_relative_to(RUNS.resolve()) or f.suffix!='.png':raise ValueError('无效图片')
    return self.send(f.read_bytes(),'image/png')
   if path.startswith('/math-pages/'):
    name=path.rsplit('/',1)[-1]
    if not re.fullmatch(r'w[1-5]-p[0-9]{1,3}\.png',name):raise ValueError('无效课件图')
    return self.send_file(ROOT/'math-pages'/name,'image/png')
   if path=='/knowledge':
    seed_path=DATA/'knowledge.json'
    if not seed_path.exists():shutil.copy2(ROOT.parent/'学习知识库数据.json',seed_path)
    seed_bytes=seed_path.read_bytes();seed=json.loads(seed_bytes.decode('utf-8'))
    html=(ROOT.parent/'我的学习知识库.html').read_text(encoding='utf-8');html=re.sub(r'(<script id="seed" type="application/json">).*?(</script>)',lambda m:m[1]+json.dumps(seed,ensure_ascii=False).replace('</','<\\/')+m[2],html,flags=re.S)
    html=html.replace('浏览器不执行C/Java/Python。','选择一种语言打开可运行例题；已整理片段会补齐明确的演示调用与入口。自定义代码仍需说明输入和调用方式。').replace('日常编辑自动保存。','编辑同步保存到本机。')
    html=html.replace('let qs=data.quizzes.filter(q=>q.topic===id||(x.related||[]).includes(q.topic));','let qs=data.quizzes.filter(q=>q.topic===id);if(!qs.length)qs=data.quizzes.filter(q=>(x.related||[]).includes(q.topic));')
    revision=hashlib.sha256(seed_bytes).hexdigest()
    addition='if(JSON.stringify(data)!==JSON.stringify(seed)){try{localStorage.setItem("learning-atlas-workbench-draft-backup",JSON.stringify(data))}catch(e){}}data=structuredClone(seed);let knowledgeRevision='+json.dumps(revision)+',knowledgeSaveQueue=Promise.resolve();const knowledgeContent=x=>JSON.stringify({...x,savedAt:0});let knowledgeCommitted=knowledgeContent(data);const previousSave=save;save=function(){const content=knowledgeContent(data);if(content===knowledgeCommitted)return knowledgeSaveQueue;previousSave();const snapshot=JSON.stringify(data);knowledgeSaveQueue=knowledgeSaveQueue.catch(()=>{}).then(async()=>{if(content===knowledgeCommitted)return {saved:true,revision:knowledgeRevision};const r=await fetch("/api/knowledge",{method:"POST",headers:{"Content-Type":"application/json","X-Study-Token":'+json.dumps(TOKEN)+',"X-Knowledge-Revision":knowledgeRevision},body:snapshot});const result=await r.json();if(!r.ok)throw new Error(result.error||"笔记写入失败");knowledgeRevision=result.revision;knowledgeCommitted=content;return result}).catch(e=>{document.getElementById("saveinfo").textContent="本机保存失败，请导出备份："+e.message;toast(e.message);throw e});return knowledgeSaveQueue;};'
    addition+='document.addEventListener("click",e=>{let b=e.target.closest("[data-workbench],[data-workcode]");if(!b)return;let x=data.cards.find(x=>x.id===route()[1]);if(!x)return;if(b.dataset.workbench){let lang=Object.keys(x.code||{})[0];if(lang)parent.postMessage({type:"study-code",topic:x.id,title:x.title,language:lang,source:x.code[lang]},location.origin);else parent.postMessage({type:"study-notebook",topic:x.id},location.origin);}else parent.postMessage({type:"study-code",topic:x.id,title:x.title,language:b.dataset.workcode,source:x.code[b.dataset.workcode]},location.origin);});const previousTopic=topicView;topicView=function(id){let html=previousTopic(id);let x=data.cards.find(x=>x.id===id);if(!x)return html;html=html.replace("<h3>相关知识</h3>","<h3>连接到可运行实验</h3><div class=actions><button data-workbench=1>运行关联完整例题</button></div><h3>相关知识</h3>");for(let lang of Object.keys(x.code||{})){html=html.replace("<summary>"+esc(lang)+"</summary>","<summary>"+esc(lang)+"</summary><button data-workcode=\\\""+esc(lang)+"\\\">打开可运行例题</button>");}return html;};render();'
    before,after=html.rsplit('</script>',1);html=before+'\n/* WORKBENCH_START */\n'+addition+'\n/* WORKBENCH_END */\n</script>'+after
    graph_script=(ROOT/'graph_lessons.js').read_text(encoding='utf-8')+'\n'+(ROOT/'search_demo.js').read_text(encoding='utf-8')+'\n'+(ROOT/'math_lessons.js').read_text(encoding='utf-8')+'\n'+(ROOT/'function_graphs.js').read_text(encoding='utf-8')+'\n'+(ROOT/'matrix_graphs.js').read_text(encoding='utf-8')+'\n'+(ROOT/'skeletal_walk.js').read_text(encoding='utf-8')
    html=html.replace('</body>','<script src="/knowledge_bridge.js"></script><script data-graph-extension>'+graph_script+'</script></body>')
    return self.send(html.encode('utf-8'),'text/html; charset=utf-8')
   if path.startswith('/课堂笔记/'):
    name=urllib.parse.unquote(path.rsplit('/',1)[-1]);f=ROOT.parent/'课堂笔记'/name
    if name not in ['笔记 2026年9月17日.pdf','笔记 2026年9月20日.pdf','笔记 2026年9月22日.pdf']:raise ValueError('无效笔记')
    return self.send(f.read_bytes(),'application/pdf')
   if path=='/':
    return self.send((ROOT/'index.html').read_text(encoding='utf-8').replace('__TOKEN__',TOKEN).encode(),'text/html; charset=utf-8')
   if path in ['/app.js','/app.css','/knowledge_bridge.js','/learning_extra.js','/graph_platform.js','/graph_lessons.js','/lecture_view.js','/lesson_cells.js','/transcript_view.js','/navigation_view.js','/lecture_layout.js','/canonical_entry.js','/course_hub.js','/local_courses.js','/system_resources.js','/lecture8_visual.js','/resource_view.js','/study_overview.js','/course_mindmap.js','/problem_workspace.js','/mobile.js','/mobile.css']:
    return self.send((ROOT/path[1:]).read_bytes(),'text/javascript; charset=utf-8' if path.endswith('.js') else 'text/css; charset=utf-8')
   return self.reply({'error':'找不到页面'},404)
  except Exception as e:self.reply({'error':str(e)},404)
 def do_POST(self):
  if not self.host_ok() or self.headers.get('Origin') not in [BASE,'http://localhost:'+str(PORT),'http://study.localhost:'+str(PORT),None] or self.headers.get('X-Study-Token')!=TOKEN:return self.reply({'error':'Request denied'},403)
  size=int(self.headers.get('Content-Length','0'))
  if size<1 or size>(128_000_000 if self.path=='/api/learning/import' else 12_500_000 if self.path.startswith('/api/learning/') else 4_000_000):return self.reply({'error':'请求大小不正确'},400)
  try:
   b=json.loads(self.rfile.read(size));path=self.path
   if path=='/api/snippet':
    source=b.get('source','')
    if not isinstance(source,str) or len(source)>200000:raise ValueError('代码格式不正确')
    rules=next(x for x in MODEL['notebooks'] if x['id']=='py-turing')['fixtures']['rules.txt']
    prepared=prepare(b.get('topic'),b.get('language'),source,rules)
    return self.reply(prepared or {'cells':[{'title':'自定义片段','code':source}],'fixtures':{},'topics':[b.get('topic')],'lead':'自定义片段：需要提供完整入口、输入与依赖；缺少入口时会提示补齐。'})
   if path=='/api/transcript-import':return self.reply(transcript_store.import_caption(b,ROOT,CONFIG['python']))
   if path=='/api/lesson-cell':return self.reply(lesson_sessions.execute(b,CONFIG['python'],ROOT))
   if path=='/api/video-pin':
    subprocess.Popen([CONFIG['python'],ROOT/'video_pin.py'],cwd=ROOT,stdout=(DATA/'video-pin.log').open('ab'),stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    return self.reply({'message':'已打开置顶窗口选择器；请选独立录播窗口，再点置顶'})
   if path=='/api/run':return self.reply({'job':job(b)})
   if path=='/api/grade':
    exercise=next(x for x in PRACTICES if x['id']==b.get('id'));source=b.get('source','')
    if not isinstance(source,str) or len(source)>200000:raise ValueError('代码格式不正确')
    language=exercise['language'];tests=exercise['tests']
    if language=='Python':payload={'language':language,'source':source+'\n'+tests,'cells':[source,tests]}
    elif language=='Java':payload={'language':language,'source':'import java.util.*;\npublic class Main {\n'+source+'\n'+tests+'\n}'}
    else:payload={'language':language,'source':'#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <stdbool.h>\n'+source+'\n'+tests}
    return self.reply({'job':job(payload),'grading':'仅依据所列公开测试；不自动证明正确性或复杂度'})
   if path=='/api/float':
    context={'id':str(b.get('id','lecture:general'))[:180],'title':str(b.get('title','我的讲座笔记'))[:300],'course':str(b.get('course','我的学习'))[:100],'week':str(b.get('week',''))[:30]}
    p=DATA/'floating-request.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(context,ensure_ascii=False),encoding='utf-8');tmp.replace(p)
    subprocess.Popen([CONFIG['python'],ROOT/'floating_notes.py'],cwd=ROOT,stdout=(DATA/'floating.log').open('ab'),stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    return self.reply({'message':'已打开置顶悬浮笔记；输入后自动保存到本机'})
   if path=='/api/open':return self.reply(open_editor(b))
   if path=='/api/state':
    if not isinstance(b,dict):raise ValueError('状态无效')
    p=DATA/'study-state.json'
    with LOCK:
     tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(b,ensure_ascii=False),encoding='utf-8');tmp.replace(p)
    return self.reply({'saved':True})
   if path=='/api/source-bundle':
    files={'main.c':str(b.get('source',''))}
    for name,content in b.get('fixtures',{}).items():
     if not re.fullmatch(r'[A-Za-z0-9_.-]{1,80}',name) or name=='main.c':raise ValueError('源文件名称无效')
     files[name]=str(content)
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as archive:
     for name,content in files.items():archive.writestr(name,content)
    return self.reply({'zip':base64.b64encode(buffer.getvalue()).decode('ascii')})
   if path=='/api/knowledge':
    if b.get('schema')!=2 or not isinstance(b.get('cards'),list):raise ValueError('知识库格式无效')
    p=DATA/'knowledge.json'
    with LOCK:
     current=hashlib.sha256(p.read_bytes()).hexdigest()
     if self.headers.get('X-Knowledge-Revision')!=current:return self.reply({'error':'知识库已有更新。请先导出当前草稿备份，再刷新载入新版；旧页面不会覆盖新内容。'},409)
     tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(b,ensure_ascii=False),encoding='utf-8');tmp.replace(p)
     revision=hashlib.sha256(p.read_bytes()).hexdigest()
    return self.reply({'saved':True,'revision':revision})
   if path=='/api/mobile-toggle':return self.reply(companion_server.start() if b.get('enabled') else companion_server.close())
   if path=='/api/learning/import':return self.reply(learning_companion.import_backup(b))
   if path=='/api/learning/grade':return self.reply(learning_companion.grade(b))
   if path=='/api/learning/mistake':return self.reply(learning_companion.save_mistake(b))
   if path=='/api/learning/drawing':return self.reply(learning_companion.save_drawing(b))
   if path=='/api/learning/score':return self.reply(learning_companion.save_score(b))
   if path=='/api/learning/correction':return self.reply(learning_companion.update_mistake(b))
   if path=='/api/learning/reference':return self.reply(learning_companion.reference_check(b))
   if path=='/api/project/java':return self.reply(start_java())
   if path=='/api/project/open':
    subprocess.Popen([CONFIG['vscode'],str(project_folder())],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);return self.reply({'message':'已打开完整项目文件夹'})
   if path=='/api/tool':
    key=b.get('tool');exe=CONFIG.get(key)
    if key not in ['arduino','android','figma'] or not exe or not pathlib.Path(exe).exists():raise ValueError('尚未找到此工具，可用资料里的官网入口')
    args=[exe,str(ROOT.parent/'smart-desk-android')] if key=='android' else [exe]
    subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);return self.reply({'message':'已启动工具'+('并打开贯穿项目的安卓端' if key=='android' else '')})
   if path=='/api/product/simulate':
    v=float(b['temperature'])
    if not -50<=v<=100:raise ValueError('教学温度应在-50到100之间')
    command_value='on' if v>=28 else 'off'
    with db() as con:con.execute('INSERT INTO telemetry(temperature,command,created) VALUES(?,?,?)',(v,command_value,time.time()))
    if JAVA and JAVA.poll() is None:
     req=urllib.request.Request('http://127.0.0.1:18867/data',data=str(v).encode(),method='POST')
     with urllib.request.urlopen(req,timeout=2) as r:r.read()
    return self.reply({'stored':True,'command':command_value})
   if path=='/api/quit':
    if JAVA:kill(JAVA)
    self.reply({'message':'工作台已退出'});threading.Thread(target=self.server.shutdown,daemon=True).start();return
   self.reply({'error':'未知操作'},404)
  except Exception as e:self.reply({'error':str(e)},400)
if __name__=='__main__':
 server=ThreadingHTTPServer(('127.0.0.1',PORT),Handler);(DATA/'instance.json').write_text(json.dumps({'port':PORT,'pid':os.getpid()}),encoding='utf-8')
 try:
  server.serve_forever()
 finally:
  if JAVA:kill(JAVA)
  companion_server.close()
  lesson_sessions.close_all()
  server.server_close()
