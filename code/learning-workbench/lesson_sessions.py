import json,pathlib,queue,re,subprocess,threading,time
SESSIONS={};GUARD=threading.Lock()
def close_all():
 with GUARD:
  for s in SESSIONS.values():
   if s['process'].poll() is None:s['process'].kill()
  SESSIONS.clear()
def execute(body,python,root):
 key=str(body.get('session',''));source=body.get('source','')
 if not re.fullmatch(r'[A-Za-z0-9_-]{1,90}',key) or not isinstance(source,str) or len(source)>200000:raise ValueError('单元或会话无效')
 with GUARD:
  for old in list(SESSIONS):
   if time.monotonic()-SESSIONS[old]['updated']>1800:
    SESSIONS.pop(old)['process'].kill()
  if body.get('reset') and key in SESSIONS:SESSIONS.pop(key)['process'].kill()
  if body.get('close'):
   if key in SESSIONS:SESSIONS.pop(key)['process'].kill()
   return {'output':'解释器已关闭；代码仍保留','exitCode':0}
  if key not in SESSIONS:
   if len(SESSIONS)>=8:raise ValueError('最多保留8个解释器，请先重启或关闭一个实验')
   cwd=pathlib.Path(root)/'data'/'kernels'/key;cwd.mkdir(parents=True,exist_ok=True)
   for name,content in body.get('fixtures',{}).items():
    if not re.fullmatch(r'[A-Za-z0-9_.-]{1,80}',name):raise ValueError('附属文件名无效')
    (cwd/name).write_text(str(content)[:100000],encoding='utf-8')
   p=subprocess.Popen([python,'-u',str(pathlib.Path(root)/'lesson_kernel.py')],cwd=cwd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,encoding='utf-8',creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
   responses=queue.Queue()
   def reader(proc=p,q=responses):
    for line in proc.stdout:q.put(line)
    q.put(None)
   threading.Thread(target=reader,daemon=True).start()
   SESSIONS[key]={'process':p,'cwd':cwd,'lock':threading.Lock(),'responses':responses,'updated':time.monotonic()}
  s=SESSIONS[key]
 with s['lock']:
  for name,content in body.get('fixtures',{}).items():
   if not re.fullmatch(r'[A-Za-z0-9_.-]{1,80}',name):raise ValueError('附属文件名无效')
   (s['cwd']/name).write_text(str(content)[:100000],encoding='utf-8')
  s['updated']=time.monotonic();start=time.monotonic()
  try:
   s['process'].stdin.write(json.dumps({'source':source,'stdin':str(body.get('stdin',''))[:100000],'cell':body.get('cell',1)},ensure_ascii=False)+'\n');s['process'].stdin.flush()
   response=s['responses'].get(timeout=20)
   if response is None:raise RuntimeError('解释器已退出，请重启')
   result=json.loads(response);result['plots']=['/api/lesson-plot/'+key+'/'+name for name in result.get('plots',[]) if re.fullmatch(r'plot-[a-f0-9]{32}\.png',name)];result['seconds']=round(time.monotonic()-start,2);return result
  except queue.Empty:
   s['process'].kill()
   with GUARD:SESSIONS.pop(key,None)
   raise ValueError('单元运行超过20秒，解释器已停止；请重启并减小输入')
