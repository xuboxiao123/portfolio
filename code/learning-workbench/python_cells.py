"""Runs a notebook from a clean namespace, keeping state between its cells."""
import ast,json,sys,pathlib,traceback,os
os.environ.setdefault('MPLBACKEND','Agg')
payload=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
scope={'__name__':'__main__'};failed=False
for i,source in enumerate(payload['cells']):
 print('\n=== 单元 '+str(i+1)+' ===',flush=True)
 try:
  tree=ast.parse(source,filename='单元'+str(i+1))
  for node in tree.body:
   if isinstance(node,ast.Expr):
    value=eval(compile(ast.Expression(node.value),'单元'+str(i+1),'eval'),scope)
    if value is not None:print(repr(value),flush=True)
   else:exec(compile(ast.Module(body=[node],type_ignores=[]),'单元'+str(i+1),'exec'),scope)
 except Exception:
  failed=True;traceback.print_exc();break
try:
 import matplotlib.pyplot as plt
 for i,n in enumerate(plt.get_fignums()):plt.figure(n).savefig('plot-'+str(i)+'.png',dpi=140,bbox_inches='tight')
except ImportError:pass
sys.exit(1 if failed else 0)
