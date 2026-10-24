import pathlib,json,urllib.request,subprocess,sys,time,webbrowser,os
root=pathlib.Path(__file__).resolve().parent
port=18765
for candidate in range(18765,18785):
 try:
  with urllib.request.urlopen('http://127.0.0.1:'+str(candidate)+'/api/health',timeout=.4) as r:data=json.load(r)
  if data.get('app')=='fullstack-study-v1':port=candidate;break
 except Exception:
  import socket
  with socket.socket() as probe:
   try:probe.bind(('127.0.0.1',candidate));port=candidate;break
   except OSError:continue
try:
 with urllib.request.urlopen('http://127.0.0.1:'+str(port)+'/api/health',timeout=.4) as r:ready=json.load(r).get('app')=='fullstack-study-v1'
except Exception:ready=False
if not ready:
 log=(root/'launch.log').open('ab');subprocess.Popen([sys.executable,str(root/'server.py'),str(port)],cwd=root,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
 for _ in range(100):
  try:
   with urllib.request.urlopen('http://127.0.0.1:'+str(port)+'/api/health',timeout=.3) as r:ready=json.load(r).get('app')=='fullstack-study-v1'
   if ready:break
  except Exception:time.sleep(.1)
if ready:webbrowser.open('http://study.localhost:'+str(port)+'/')
else:
 if os.name=='nt':os.startfile(str(root/'launch.log'))
