"""Read-only access to explicitly indexed local learning materials."""
import json
from pathlib import Path

INDEX = Path(__file__).resolve().parent / 'data' / 'supplementary-index.json'
ALLOWED_ROOT = Path(r'F:\研究生作业合集\研一第一学期').resolve()

def load():
    return json.loads(INDEX.read_text(encoding='utf-8'))

def public_index():
    data=load()
    return {**data, 'files':[{k:v for k,v in item.items() if k!='path'} for item in data['files']]}

def file(ident):
    row=next((x for x in load()['files'] if x['id']==ident),None)
    if row is None: raise ValueError('资料未登记')
    path=Path(row['path']).resolve()
    if not path.is_relative_to(ALLOWED_ROOT) or not path.is_file():
        raise ValueError('原文件不在已登记的F盘资料目录，或文件已移走')
    return row,path

def preview(ident):
    row,path=file(ident)
    if row['kind'] not in ['code','notebook','text','data']:
        raise ValueError('该文件不支持文字预览')
    if path.stat().st_size>4*1024*1024:raise ValueError('文件较大，请下载后查看')
    content=path.read_text(encoding='utf-8-sig',errors='replace')
    if row['kind']=='notebook':
        nb=json.loads(content)
        return {'cells':[{'type':c.get('cell_type'),'source':''.join(c.get('source',[]))} for c in nb.get('cells',[])], 'review':'原代码预览，未自动执行'}
    return {'text':content[:160000], 'truncated':len(content)>160000}
