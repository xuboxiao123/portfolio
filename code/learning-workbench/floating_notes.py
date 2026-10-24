"""A local, movable, always-on-top lecture notebook. No recording or upload."""
import pathlib,json,sqlite3,time,tkinter as tk
from tkinter import ttk
import sys,hashlib,os,ctypes
from contextlib import contextmanager
ROOT=pathlib.Path(__file__).resolve().parent;DATA=ROOT/'data';DATA.mkdir(exist_ok=True)
REQUEST=DATA/'floating-request.json';DB=DATA/'product.sqlite'
integration_temp=None
if '--integration-test' in sys.argv:
 import tempfile
 integration_temp=tempfile.TemporaryDirectory()
 ROOT=pathlib.Path(integration_temp.name);DATA=ROOT/'data';DATA.mkdir()
 REQUEST=DATA/'floating-request.json';DB=DATA/'product.sqlite'
@contextmanager
def connect(path=DB):
 con=sqlite3.connect(path,timeout=8)
 con.execute('CREATE TABLE IF NOT EXISTS lecture_notes(id TEXT PRIMARY KEY,title TEXT,course TEXT,week TEXT,body TEXT,updated REAL)')
 try:
  yield con
  con.commit()
 except Exception:
  con.rollback();raise
 finally:con.close()
def write_note(context,body,path=DB):
 with connect(path) as con:con.execute('INSERT INTO lecture_notes VALUES(?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET title=excluded.title,course=excluded.course,week=excluded.week,body=excluded.body,updated=excluded.updated',(context['id'],context.get('title','讲座笔记'),context.get('course','我的学习'),str(context.get('week','')),body,time.time()))
def read_note(id,path=DB):
 with connect(path) as con:row=con.execute('SELECT body FROM lecture_notes WHERE id=?',(id,)).fetchone()
 return row[0] if row else ''
def self_test():
 import tempfile
 with tempfile.TemporaryDirectory() as folder:
  path=pathlib.Path(folder)/'test.sqlite';c={'id':'test','title':'测试','course':'9024','week':'3'}
  write_note(c,'heap（堆）与 pointer（指针）',path);assert read_note('test',path)=='heap（堆）与 pointer（指针）'
  root=tk.Tk();root.withdraw();root.attributes('-topmost',True);assert root.attributes('-topmost')
  editor=tk.Text(root);editor.insert('1.0','讲座记录');assert editor.get('1.0','end-1c')=='讲座记录';root.destroy()
 print('Floating notebook: topmost, Unicode editor and persistent storage verified')
if '--self-test' in sys.argv:self_test();sys.exit(0)
# One window per workbench directory. A second request is picked up by the first.
mutex=None
if os.name=='nt':
 from ctypes import wintypes
 kernel=ctypes.WinDLL('kernel32',use_last_error=True)
 kernel.CreateMutexW.argtypes=[wintypes.LPVOID,wintypes.BOOL,wintypes.LPCWSTR];kernel.CreateMutexW.restype=wintypes.HANDLE
 mutex=kernel.CreateMutexW(None,False,'Local\\StudyLectureNotes_'+hashlib.sha256(str(ROOT).encode()).hexdigest()[:20])
 if ctypes.get_last_error()==183:sys.exit(0)
root=tk.Tk();root.title('讲座悬浮笔记');root.configure(bg='#edf5f1');root.attributes('-topmost',True)
root.geometry('490x570+'+str(max(20,root.winfo_screenwidth()-520))+'+80');root.minsize(330,220)
style=ttk.Style(root);style.configure('TLabel',font=('Microsoft YaHei',10));style.configure('TButton',font=('Microsoft YaHei',10))
frame=ttk.Frame(root,padding=12);frame.pack(fill='both',expand=True)
top=tk.BooleanVar(value=True);ttk.Checkbutton(frame,text='置顶 · 边看讲座边记',variable=top,command=lambda:root.attributes('-topmost',top.get())).pack(anchor='w')
title=tk.StringVar();course=tk.StringVar();week=tk.StringVar();status=tk.StringVar(value='笔记保存在本机，不录音、不上传')
ttk.Label(frame,text='知识点 / 讲座名称').pack(anchor='w',pady=(10,0));title_edit=ttk.Entry(frame,textvariable=title);title_edit.pack(fill='x')
row=ttk.Frame(frame);row.pack(fill='x',pady=8)
ttk.Combobox(row,textvariable=course,values=['9020','9021','9024','本科','我的学习'],width=15).pack(side='left');ttk.Label(row,text='  Week（周）').pack(side='left');ttk.Entry(row,textvariable=week,width=8).pack(side='left')
ttk.Label(frame,text='先写具体例子，再写“为什么”；不懂的地方也留下来。',wraplength=440).pack(anchor='w')
editor_frame=ttk.Frame(frame);editor_frame.pack(fill='both',expand=True,pady=8)
text=tk.Text(editor_frame,wrap='word',font=('Microsoft YaHei',11),undo=True,bg='white',fg='#183a48',relief='flat',padx=10,pady=10)
scroll=ttk.Scrollbar(editor_frame,command=text.yview);text.configure(yscrollcommand=scroll.set);scroll.pack(side='right',fill='y');text.pack(side='left',fill='both',expand=True)
buttons=ttk.Frame(frame);buttons.pack(fill='x');ttk.Label(frame,textvariable=status,wraplength=440).pack(anchor='w',pady=(8,0))
context={'id':'lecture:general','title':'我的讲座记录','course':'我的学习','week':''};loading=False;pending=None;seen_request=0;folded=False
def save():
 global pending
 if loading:return
 context.update(title=title.get() or '讲座笔记',course=course.get() or '我的学习',week=week.get())
 try:write_note(context,text.get('1.0','end-1c'));status.set('已保存到本机 · '+time.strftime('%H:%M:%S'))
 except Exception as error:status.set('保存失败：'+str(error))
 pending=None
def changed(*args):
 global pending
 if loading:return
 if pending:root.after_cancel(pending)
 pending=root.after(600,save)
def modified(event):
 if text.edit_modified():changed();text.edit_modified(False)
text.bind('<<Modified>>',modified)
for value in [title,course,week]:value.trace_add('write',changed)
def load(new):
 global context,loading
 save();loading=True;context={'id':str(new.get('id','lecture:general')),'title':new.get('title','讲座笔记'),'course':new.get('course','我的学习'),'week':new.get('week','')}
 with connect() as con:row=con.execute('SELECT title,course,week,body FROM lecture_notes WHERE id=?',(context['id'],)).fetchone()
 if row:context.update(title=row[0],course=row[1],week=row[2]);body=row[3]
 else:body=''
 title.set(context['title']);course.set(context['course']);week.set(str(context['week']));text.delete('1.0','end');text.insert('1.0',body);text.edit_modified(False);loading=False
 status.set('已打开笔记；输入后自动保存');root.deiconify();root.lift()
def new_note():load({'id':'lecture:'+str(time.time_ns()),'title':'新讲座笔记','course':course.get(),'week':week.get()})
def fold():
 global folded
 folded=not folded
 if folded:editor_frame.pack_forget();root.geometry('490x240')
 else:editor_frame.pack(fill='both',expand=True,pady=8,before=buttons);root.geometry('490x570')
ttk.Button(buttons,text='立即保存',command=save).pack(side='left');ttk.Button(buttons,text='新讲座',command=new_note).pack(side='left',padx=6);ttk.Button(buttons,text='收起 / 展开',command=fold).pack(side='right')
def poll():
 global seen_request
 try:
  stamp=REQUEST.stat().st_mtime_ns if REQUEST.exists() else 0
  if stamp!=seen_request:
   new=json.loads(REQUEST.read_text(encoding='utf-8'));seen_request=stamp;load(new)
 except Exception as error:status.set('读取笔记入口失败：'+str(error))
 root.after(500,poll)
def close():
 save();(DATA/'floating-status.json').write_text(json.dumps({'open':False,'pid':os.getpid()}),encoding='utf-8');root.destroy()
root.protocol('WM_DELETE_WINDOW',close)
(DATA/'floating-status.json').write_text(json.dumps({'open':True,'pid':os.getpid(),'topmost':True}),encoding='utf-8')
loading=True;title.set(context['title']);course.set(context['course']);loading=False
root.after(50,poll)
integration_failure=[]
if integration_temp:
 root.withdraw()
 def test_edit():
  load({'id':'integration','title':'自动保存验证','course':'9024','week':'3'});root.withdraw()
  text.insert('1.0','heap（堆）：先问对象生命周期，再问硬件地址。')
 def test_restore():
  try:
   assert read_note('integration')=='heap（堆）：先问对象生命周期，再问硬件地址。'
   assert root.attributes('-topmost')
   load({'id':'other','title':'另一个讲座','course':'9021','week':'1'});root.withdraw()
   assert text.get('1.0','end-1c')==''
   load({'id':'integration'});root.withdraw()
   assert text.get('1.0','end-1c')==read_note('integration')
   assert course.get()=='9024' and week.get()=='3'
   print('PASS: actual Tk edit event → autosave → switch context → restore, topmost=True',flush=True)
  except Exception as error:integration_failure.append(error)
  finally:close()
 root.after(100,test_edit);root.after(1500,test_restore)
root.mainloop()
if integration_temp:
 integration_temp.cleanup()
 if integration_failure:raise integration_failure[0]
