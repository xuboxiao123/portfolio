import json,pathlib,sqlite3,time,secrets,re,base64,io,hashlib
from fractions import Fraction
from contextlib import contextmanager
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parent
DATA=ROOT/'data'
QUESTIONS=json.loads((ROOT/'problem_questions.json').read_text(encoding='utf-8'))
@contextmanager
def database():
 con=sqlite3.connect(DATA/'learning-companion.sqlite',timeout=15);con.row_factory=sqlite3.Row
 con.execute('CREATE TABLE IF NOT EXISTS attempts(id TEXT PRIMARY KEY,question TEXT,answer TEXT,verdict TEXT,created REAL)')
 con.execute('CREATE TABLE IF NOT EXISTS mistakes(id TEXT PRIMARY KEY,course TEXT,question TEXT,title TEXT,answer TEXT,explanation TEXT,image TEXT,correction TEXT,status TEXT,created REAL)')
 con.execute('CREATE TABLE IF NOT EXISTS scores(id TEXT PRIMARY KEY,course TEXT,title TEXT,earned REAL,maximum REAL,weight REAL,source TEXT,updated REAL)')
 con.execute('CREATE TABLE IF NOT EXISTS drawings(question TEXT PRIMARY KEY,image TEXT,updated REAL)')
 try:yield con;con.commit()
 finally:con.close()
def public_question(q):return {k:v for k,v in q.items() if k!='answer'}
def normalize_set(text,pairs=False):
 text=text.strip().replace('（','(').replace('）',')').replace('，',',').replace('；',';').replace('｛','{').replace('｝','}').replace('−','-')
 text=re.sub(r'^[A-Za-z←]+\s*=','',text).strip()
 if text in ['{}','∅','empty','空集']:return set()
 if pairs:
  matches=re.findall(r'\(\s*(-?\d+)\s*[,;]\s*(-?\d+)\s*\)',text)
  remaining=re.sub(r'\(\s*-?\d+\s*[,;]\s*-?\d+\s*\)','',text)
  if not matches or re.sub(r'[\s{},;]','',remaining):raise ValueError('请用{(0,1),(0,2)}这样的有序对集合格式。')
  return {tuple(map(int,x)) for x in matches}
 text=text.strip('{} ')
 def expand(match):
  start,end=int(match[1]),int(match[2])
  if not 0<=end-start<=1000:raise ValueError('连续集合范围过大或方向不对。')
  return ','.join(map(str,range(start,end+1)))
 text=re.sub(r'(-?\d+)\s*,\s*(?:\.\.\.|…)\s*,\s*(-?\d+)',expand,text)
 values=re.split(r'[,;\s]+',text)
 if not values or any(not re.fullmatch(r'-?\d+',x) for x in values):raise ValueError('请用{1,2,3}这样的整数集合格式。')
 return {int(x) for x in values}
def check_answer(q,answer):
 kind=q['kind'];expected=q['answer'];text=str(answer).strip()
 if not text:raise ValueError('请先填写答案。')
 if kind=='proof':return {'verdict':'needs_review','message':'证明题需要核对逻辑，不能仅凭关键词自动判为正确。请对照下面步骤检查，再把具体疑问带给GPT。','steps':q['steps']}
 if kind=='pairs':correct=normalize_set(text,True)=={tuple(p) for p in expected}
 elif kind=='set':correct=normalize_set(text)==set(expected)
 elif kind=='number':
  try:correct=Fraction(text)==Fraction(str(expected))
  except (ValueError,ZeroDivisionError):raise ValueError('请输入一个数；也可以写成3/2这样的分数。')
 elif kind=='properties':
  values={x.upper() for x in re.split(r'[,，;；\s]+',text) if x};allowed={'R','AR','S','AS','T'}
  if not values<=allowed:raise ValueError('性质请用R、AR、S、AS、T表示。')
  correct=values==set(expected)
 elif kind=='choice':
  aliases={'是':'yes','成立':'yes','true':'yes','否':'no','不是':'no','不成立':'no','false':'no'};value=aliases.get(text.lower(),text.lower())
  if value not in ['yes','no']:raise ValueError('请选择是／否。')
  correct=value==expected
 elif kind=='scalar':correct=text.lower().replace(' ','') in ['r','ℝ','\\mathbbr','实数','实数集','allrealnumbers','realnumbers']
 elif kind=='interval':
  match=re.fullmatch(r'\[\s*([-\d./]+)\s*[,，]\s*([-\d./]+)\s*\]',text.replace('−','-'))
  if not match:raise ValueError('请用[-2.5,2.5]或[-5/2,5/2]这样的闭区间格式。')
  correct=[Fraction(x) for x in match.groups()]==[Fraction(str(x)) for x in expected]
 else:raise ValueError('此题型尚不支持自动判分。')
 return {'verdict':'correct' if correct else 'incorrect','message':'答案正确。再解释一下每一步为什么成立。' if correct else '答案不匹配。下面按原题条件拆开推导；也已加入错题记录。','expected':expected,'steps':q['steps']}
def grade(body):
 q=next((x for x in QUESTIONS if x['id']==body.get('question')),None)
 if not q:raise ValueError('没有找到此题。')
 answer=str(body.get('answer',''))[:10000];result=check_answer(q,answer)
 with database() as con:
  con.execute('INSERT INTO attempts VALUES(?,?,?,?,?)',(secrets.token_hex(8),q['id'],answer,result['verdict'],time.time()))
  if result['verdict']=='incorrect':
   mistake_id=secrets.token_hex(8);con.execute('INSERT INTO mistakes VALUES(?,?,?,?,?,?,?,?,?,?)',(mistake_id,q['course'],q['id'],'PS4 '+q['label']+' · '+q['prompt'],answer,'\n'.join(q['steps']),'','','待纠错',time.time()));result['mistakeId']=mistake_id
 return result
def store_image(value):
 if not value:return ''
 if not isinstance(value,str) or len(value)>12000000:raise ValueError('图片过大，请选择8MB以内图片。')
 encoded=value.split(',',1)[-1]
 raw=base64.b64decode(encoded,validate=True)
 if len(raw)>8000000:raise ValueError('图片过大。')
 if raw.startswith(b'%PDF-'):
  from pypdf import PdfReader,PdfWriter
  reader=PdfReader(io.BytesIO(raw))
  if reader.is_encrypted or not 1<=len(reader.pages)<=200:raise ValueError('PDF需未加密且不超过200页。')
  writer=PdfWriter()
  for page in reader.pages:
   if '/AA' in page:del page['/AA']
   for annotation in page.get('/Annots',[]):
    obj=annotation.get_object()
    for key in ['/A','/AA','/JS']:
     if key in obj:del obj[key]
   writer.add_page(page)
  folder=DATA/'mistake-images';folder.mkdir(exist_ok=True);name=secrets.token_hex(16)+'.pdf'
  with (folder/name).open('wb') as f:writer.write(f)
  return name
 img=Image.open(io.BytesIO(raw));img.verify();img=Image.open(io.BytesIO(raw));img.thumbnail((2400,2400));img=img.convert('RGB')
 folder=DATA/'mistake-images';folder.mkdir(exist_ok=True);name=secrets.token_hex(16)+'.jpg';img.save(folder/name,quality=88)
 return name
def save_mistake(body):
 title=str(body.get('title','错题'))[:200];image=store_image(body.get('image'));id=secrets.token_hex(8)
 with database() as con:con.execute('INSERT INTO mistakes VALUES(?,?,?,?,?,?,?,?,?,?)',(id,str(body.get('course','9020'))[:40],str(body.get('question',''))[:100],title,str(body.get('answer',''))[:10000],str(body.get('explanation',''))[:20000],image,str(body.get('correction',''))[:20000],'待纠错',time.time()))
 return {'saved':True,'id':id,'message':'已保存到电脑错题库。照片尚未自动识别；请填写题号、转写与纠错。'}
def save_drawing(body):
 question=str(body.get('question',''))[:100];image=store_image(body.get('image'))
 if not question or not image:raise ValueError('请选择题目并先写下解题过程。')
 with database() as con:con.execute('INSERT INTO drawings VALUES(?,?,?) ON CONFLICT(question) DO UPDATE SET image=excluded.image,updated=excluded.updated',(question,image,time.time()))
 return {'saved':True,'image':image}
def save_score(body):
 course=str(body.get('course',''));id=str(body.get('id') or hashlib.sha256((course+'|'+str(body.get('title','')).strip().lower()).encode()).hexdigest()[:16])[:100];maximum=float(body.get('maximum',0));earned=float(body.get('earned',0));weight=float(body.get('weight',0))
 if course not in ['9020','9021','9024'] or maximum<=0 or not 0<=earned<=maximum or not 0<=weight<=100:raise ValueError('检查课程、得分、满分和占比。未出成绩请不要录为0。')
 with database() as con:con.execute('INSERT INTO scores VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET title=excluded.title,earned=excluded.earned,maximum=excluded.maximum,weight=excluded.weight,source=excluded.source,updated=excluded.updated',(id,course,str(body.get('title',''))[:150],earned,maximum,weight,str(body.get('source','手动登记，待与学校核对'))[:200],time.time()))
 return {'saved':True}
def update_mistake(body):
 with database() as con:
  found=con.execute('SELECT id FROM mistakes WHERE id=?',(body.get('id'),)).fetchone()
  if not found:raise ValueError('错题不存在。')
  status=body.get('status','待纠错')
  if status not in ['待纠错','已纠错','已回练']:raise ValueError('状态无效。')
  con.execute('UPDATE mistakes SET correction=?,status=? WHERE id=?',(str(body.get('correction',''))[:20000],status,body['id']))
 return {'saved':True}
def reference_check(body):
 kind=body.get('kind');answer=str(body.get('answer',''))[:10000];reference=str(body.get('reference',''))[:10000]
 if kind not in ['set','pairs','number','interval']:raise ValueError('证明、文字和图不能仅用字符串判分；请按参考解答检查步骤。')
 if not reference.strip():raise ValueError('请先输入从官方解答核对的参考值。')
 if kind in ['set','pairs']:expected=normalize_set(reference,kind=='pairs');actual=normalize_set(answer,kind=='pairs');correct=expected==actual
 elif kind=='number':correct=Fraction(answer)==Fraction(reference)
 else:
  def interval(s):
   match=re.fullmatch(r'([\[(])\s*([-\d./]+)\s*[,，]\s*([-\d./]+)\s*([\])])',s.replace('−','-').strip())
   if not match:raise ValueError('请用[-2.5,2.5]这样的区间格式。')
   return (match[1],Fraction(match[2]),Fraction(match[3]),match[4])
  correct=interval(answer)==interval(reference)
 return {'verdict':'correct' if correct else 'incorrect','message':'与所填参考值等价。参考值仍需对照官方答案确认。' if correct else '与参考值不同。检查遗漏／多出的元素、顺序、区间端点和题目条件。','steps':['本检查只比较所填参考值，不认证它是正确的官方答案。','把集合排序、分数约分后比较；区间保留开闭端点。']}
def snapshot():
 plan=json.loads((ROOT/'study_plan.json').read_text(encoding='utf-8'));knowledge=json.loads((DATA/'knowledge.json').read_text(encoding='utf-8'))
 with database() as con:
  mistakes=[dict(r) for r in con.execute('SELECT * FROM mistakes ORDER BY created DESC LIMIT 100')];scores=[dict(r) for r in con.execute('SELECT * FROM scores ORDER BY course,title')];drawings=[dict(r) for r in con.execute('SELECT * FROM drawings')]
 return {'knowledgeCards':[{k:c.get(k,'') for k in ['id','course','week','title','status','body','example']} for c in knowledge['cards'] if c['course'] in ['9020','9021','9024']],'plan':plan,'courses':[{**c,'topics':sum(x['course']==c['id'] for x in knowledge['cards']),'mastered':sum(x['course']==c['id'] and x.get('status')=='已掌握' for x in knowledge['cards'])} for c in knowledge['courses'] if c['id'] in ['9020','9021','9024']],'mistakes':mistakes,'scores':scores,'drawings':drawings,'assessment':json.loads((ROOT/'assessment_rules.json').read_text(encoding='utf-8'))}
def export_backup():
 with database() as con:result={table:[dict(r) for r in con.execute('SELECT * FROM '+table)] for table in ['mistakes','scores','drawings','attempts']}
 result['version']=1;result['assets']={}
 for row in result['mistakes']+result['drawings']:
  name=row.get('image','')
  if name and re.fullmatch(r'[a-f0-9]{32}\.(?:jpg|pdf)',name):
   p=DATA/'mistake-images'/name
   if p.exists():result['assets'][name]=base64.b64encode(p.read_bytes()).decode()
 return result
def import_backup(body):
 if body.get('version')!=1:raise ValueError('错题备份版本不正确。')
 tables={'mistakes':['id','course','question','title','answer','explanation','image','correction','status','created'],'scores':['id','course','title','earned','maximum','weight','source','updated'],'drawings':['question','image','updated'],'attempts':['id','question','answer','verdict','created']}
 for table,columns in tables.items():
  rows=body.get(table,[])
  if not isinstance(rows,list) or len(rows)>100000 or any(not isinstance(r,dict) or set(r)!=set(columns) for r in rows):raise ValueError('备份表格式不正确：'+table)
 assets=body.get('assets',{});mapping={}
 if not isinstance(assets,dict) or len(assets)>2000 or sum(len(str(v)) for v in assets.values())>90000000:raise ValueError('图片备份过大。')
 for name,value in assets.items():
  if not re.fullmatch(r'[a-f0-9]{32}\.(?:jpg|pdf)',name):raise ValueError('备份图片名称无效。')
  mapping[name]=store_image(value)
 with database() as con:
  for table,columns in tables.items():
   for row in body.get(table,[]):
    row=dict(row)
    if 'image' in row:row['image']=mapping.get(row['image'],'')
    if any(not isinstance(v,(str,int,float,type(None))) for v in row.values()):raise ValueError('记录字段无效。')
    con.execute('INSERT OR REPLACE INTO '+table+' ('+','.join(columns)+') VALUES ('+','.join('?' for _ in columns)+')',[row[k] for k in columns])
 return {'saved':True}
