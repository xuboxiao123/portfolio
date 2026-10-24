"""Local caption import, one-time translation, and persistent cache."""
import hashlib,json,pathlib,subprocess,threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit
from translate_transcript import parse_vtt
POOL=ThreadPoolExecutor(max_workers=1);ACTIVE={};LOCK=threading.Lock()
def import_caption(body,root,python):
 video=body.get('video','');url=urlsplit(video)
 if url.scheme!='https' or url.hostname!='echo360.net.au' or not url.path.startswith('/lesson/'):raise ValueError('请选择EchoVideo课堂录播')
 vtt=body.get('vtt','')
 if not isinstance(vtt,str) or len(vtt)>2000000 or not vtt.lstrip('\ufeff\r\n ').startswith('WEBVTT'):raise ValueError('请选择不超过2MB的WebVTT逐字稿')
 cues=parse_vtt(vtt)
 if not cues or len(cues)>20000:raise ValueError('逐字稿没有有效时间段，或时间段过多')
 directory=root/'data/transcripts';directory.mkdir(exist_ok=True)
 key=hashlib.sha256(video.encode()).hexdigest()[:24]
 with LOCK:
  for path in directory.glob('*.json'):
   d=json.loads(path.read_text(encoding='utf-8'))
   if d.get('video')==video:
    if d.get('complete'):return {'cached':True,'message':'这节课已有完整译文，直接使用缓存，没有重新翻译。'}
    break
  else:
   path=directory/(key+'.json');d={'video':video,'title':str(body.get('title','本节讲座'))[:180],'source':'用户导入的EchoVideo WebVTT','translated':0,'complete':False,'cues':cues}
   path.write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8');path.with_suffix('.vtt').write_text(vtt,encoding='utf-8')
  if video in ACTIVE:return {'cached':False,'message':'这节课正在翻译，不会重复启动。'}
  if len(ACTIVE)>=8:raise ValueError('已有8节课等待翻译，请稍后导入')
  ACTIVE[video]=True
  def work():
   try:
    with path.with_suffix('.log').open('ab') as log:
     result=subprocess.run([python,str(root/'translate_transcript.py'),str(path)],cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=3600,creationflags=subprocess.CREATE_NO_WINDOW)
     if result.returncode:raise RuntimeError('本机翻译未完成，请重新导入重试；已完成的译文保留。')
   except Exception:
    latest=json.loads(path.read_text(encoding='utf-8'));latest['error']='本机翻译已停止，未完成。重新导入可接着处理，已译内容不会重复翻译。'
    temporary=path.with_suffix('.error-tmp');temporary.write_text(json.dumps(latest,ensure_ascii=False),encoding='utf-8');temporary.replace(path)
   finally:
    with LOCK:ACTIVE.pop(video,None)
  POOL.submit(work)
 return {'cached':False,'message':'已开始本机自动翻译；译完停止并永久保存，不调用GPT。'}
