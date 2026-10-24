"""Translate saved English WebVTT locally. No lecture text leaves this machine."""
import sys,json,pathlib,re,html,os
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'runtime/translation'))
def parse_vtt(text):
 cues=[]
 for block in re.split(r'\r?\n\s*\r?\n',text.lstrip('\ufeff')):
  lines=block.splitlines()
  for i,line in enumerate(lines):
   m=re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})',line)
   if m:
    clean=html.unescape(re.sub(r'<[^>]*>','', ' '.join(lines[i+1:]))).strip()
    if clean:cues.append({'start':m[1],'end':m[2],'en':clean,'zh':''})
    break
 return cues
def translate_file(path):
 data=json.loads(path.read_text(encoding='utf-8'))
 if data.get('complete') and all(c.get('zh') for c in data['cues']):return
 data.pop('error',None)
 import ctranslate2,sentencepiece
 p=ROOT/'runtime/translation-model/translate-en_zh-1_9'
 sp=sentencepiece.SentencePieceProcessor(model_proto=(p/'sentencepiece.model').read_bytes())
 # The native Windows library cannot open this model using a Chinese filename.
 previous=os.getcwd();os.chdir(p)
 try:t=ctranslate2.Translator('model',device='cpu',compute_type='int8',intra_threads=4)
 finally:os.chdir(previous)
 for start in range(0,len(data['cues']),32):
  batch=[c for c in data['cues'][start:start+32] if not c.get('zh')]
  if not batch:continue
  results=t.translate_batch([sp.encode(c['en'],out_type=str) for c in batch],beam_size=2,max_decoding_length=180)
  for cue,result in zip(batch,results):cue['zh']=sp.decode(result.hypotheses[0]).replace('▁',' ').strip()
  data['translated']=sum(bool(c.get('zh')) for c in data['cues'])
  tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');tmp.replace(path)
  print(data['translated'],flush=True)
 data['complete']=True;tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');tmp.replace(path)
if __name__=='__main__':translate_file(pathlib.Path(sys.argv[1]).resolve())
