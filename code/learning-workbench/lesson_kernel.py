"""Local notebook worker. Namespace persists until the user restarts it."""
import ast,builtins,contextlib,io,json,pathlib,sys,traceback,os,uuid
os.environ.setdefault('MPLBACKEND','Agg')
sys.stdin.reconfigure(encoding='utf-8');sys.stdout.reconfigure(encoding='utf-8')
scope={'__name__':'__main__'}
class BoundedOutput(io.StringIO):
 def write(self,text):
  if self.tell()+len(text)>250000:raise RuntimeError('输出过多，请减少循环次数')
  return super().write(text)
for line in sys.stdin:
 out=BoundedOutput();status=0;plots=[]
 try:
  command=json.loads(line);inputs=iter(command.get('stdin','').splitlines())
  def read_input(prompt=''):
   print(prompt,end='')
   try:return next(inputs)
   except StopIteration:raise EOFError('本单元需要更多输入，请在本单元输入框按行填写后重试')
  scope['__builtins__']={**vars(builtins),'input':read_input}
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):
   tree=ast.parse(command['source'],filename='单元 '+str(command.get('cell',1)))
   for node in tree.body:
    if isinstance(node,ast.Expr):
     value=eval(compile(ast.Expression(node.value),'<cell>','eval'),scope)
     if value is not None:print(repr(value))
    else:exec(compile(ast.Module(body=[node],type_ignores=[]),'<cell>','exec'),scope)
 except BaseException:
  status=1
  try:traceback.print_exc(file=out)
  except RuntimeError:pass
 if 'matplotlib.pyplot' in sys.modules:
  try:
   plt=sys.modules['matplotlib.pyplot']
   for n in plt.get_fignums()[:8]:
    file='plot-'+uuid.uuid4().hex+'.png';plt.figure(n).savefig(file,dpi=120,bbox_inches='tight');plots.append(file)
   plt.close('all')
  except Exception:traceback.print_exc(file=out);status=1
 print(json.dumps({'output':out.getvalue(),'exitCode':status,'plots':plots},ensure_ascii=False),flush=True)
