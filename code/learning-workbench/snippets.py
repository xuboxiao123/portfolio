"""Explicit teaching inputs and entry points for knowledge-card examples."""
def prepare(topic,language,source,rules=''):
    search_books={'dfs-path':'c-dfs-detailed','dfs-predecessor':'c-dfs-detailed','bfs-path':'c-bfs-detailed','graph-cycle':'c-search-applications','components':'c-search-applications','hamilton-path':'c-hamilton-euler','euler-path':'c-hamilton-euler'}
    if topic in search_books and language=='C' and '#include "Search.h"' in source:
        import json,pathlib
        model=json.loads((pathlib.Path(__file__).parent/'model.json').read_text(encoding='utf-8'))
        book=next(b for b in model['notebooks'] if b['id']==search_books[topic])
        return {'cells':[{'title':'main.c · 明确输入与检查','code':source}], 'fixtures':book['fixtures'], 'lead':book['lead'], 'topics':[topic]}
    if topic in ['linked','brackets'] and language in ['C','Java','Python']:
        return {'cells':[{'title':'完整程序与检查','code':source}], 'fixtures':{}, 'lead':'完整教学程序，直接运行相同输入并观察节点或栈状态。', 'topics':[topic]}
    if language=='C' and topic in ['graphmatrix','graphedges','graphlist'] and '#include "Graph.h"' in source:
        import json,pathlib
        model=json.loads((pathlib.Path(__file__).parent/'model.json').read_text(encoding='utf-8'))
        book=next(b for b in model['notebooks'] if b['id']=='c-'+topic+'-adt')
        return {'cells':[{'title':'main.c · 使用Graph ADT接口','code':source}], 'fixtures':book['fixtures'], 'lead':book['lead'], 'topics':[topic]}
    before=after='';fixtures={}
    if language=='C':
        cases={
          'numbers':('', 'printf("gcd(42,30) = %d\\n", gcd(42,30));', True),
          'cbasic':('', 'int a[]={2,4,6}; printf("sum = %d\\n",sum(a,3));',True),
          'memory':('', 'int *p=make_value(); if(!p){puts("分配失败");return 1;} printf("value = %d\\n",*p); free(p);',True),
          'sets':('', 'printf("交集位掩码 = %u\\n",intersection); for(int i=0;i<8;i++)if(intersection&(1u<<i))printf("元素 %d\\n",i);',False),
          'function':('int a[]={-3,-2,-1,0,1,2,3}; int n=7,out[7],count=0;', 'for(int i=0;i<count;i++)printf("%d ",out[i]); puts("");',False),
          'matrix':('', 'rows[0][1]=7; printf("第一行=%d，第二行=%d\\n",rows[0][1],rows[1][1]);',False),
          'graphedges':('', 'printf("顶点=%d，边=%d；首边=(%d,%d)\\n",nV,nE,edges[0].u,edges[0].v);',False),
          'graphmatrix':('', 'printf("0连接2=%d，2连接0=%d\\n",M[0][2],M[2][0]);',False),
          'graphlist':('', 'Node *node=malloc(sizeof *node); if(!node)return 1; node->v=2; node->next=adj[0]; adj[0]=node; printf("0的邻居=%d\\n",adj[0]->v); free(node);',False),
        }
        if topic not in cases:return None
        before,after,function=cases[topic]
        headers='#include <stdio.h>\n#include <stdlib.h>\n'
        driver='\nint main(void) {\n    /* 明确的教学输入，可自行修改。 */\n    '+before+'\n    '+after+'\n    return 0;\n}\n'
        code=headers+source+driver if function else headers+'\nint main(void) {\n'+before+'\n'+source+'\n'+after+'\nreturn 0;\n}\n'
    elif language=='Java':
        cases={
          'numbers':('', 'System.out.println("gcd(42,30) = "+gcd(42,30));',True),
          'sets':('Set<Integer> a=new HashSet<>(Arrays.asList(1,3,5)),b=new HashSet<>(Arrays.asList(3,4));','System.out.println("并集="+new TreeSet<>(union));System.out.println("原集合="+new TreeSet<>(a));',False),
          'function':('int[] domain={-3,-2,-1,0,1,2,3}; Set<Integer> targets=new HashSet<>(Arrays.asList(1,9)); List<Integer> preimage=new ArrayList<>();','System.out.println("原像="+preimage);',False),
          'matrix':('','rows[0][1]=7;System.out.println("第一行="+rows[0][1]+"，第二行="+rows[1][1]);',False),
          'graphedges':('','System.out.println("顶点="+V+"；首边="+Arrays.toString(edges.get(0)));',False),
          'graphmatrix':('','System.out.println("0连接2="+M[0][2]+"，2连接0="+M[2][0]);',False),
          'graphlist':('int V=5;','System.out.println(adj);',False),
        }
        if topic not in cases:return None
        before,after,function=cases[topic]
        code='import java.util.*;\npublic class Main {\n'
        if function:code+=source+'\n'
        code+='public static void main(String[] args) {\n// 明确的教学输入，可自行修改。\n'+before+'\n'+('' if function else source)+'\n'+after+'\n}\n}\n'
    elif language=='Python':
        outputs={'numbers':'print("gcd(42,30) =",gcd(42,30))','function':'print("原像 =",sorted(preimage))','matrix':'rows[0][1]=7\nprint(rows)','bfsdfs':'adj=[[1,2],[0,3],[0,3],[1,2,4],[3]]\nprint("BFS =",bfs(adj,0))','graphedges':'print("边数组 =",edges)','graphmatrix':'print("矩阵 =",M)','graphlist':'print("邻接表 =",adj)','tmrules':'print(new_state,new_bit,direction)','tmparser':'print("规则数 =",len(rules))','tmengine':'print("输入6的停机配置：",run(rules,6))','classfractions':'print("0.12(34) =",fraction("12","34"))','classautomata':'print("旧行 =",old)\nprint("新行 =",new)'}
        if topic=='tmparser':fixtures={'rules.txt':rules}
        if topic=='tmengine':
            fixtures={'rules.txt':rules}
            before='rules={}\nwith open("rules.txt",encoding="utf-8") as file:\n    for raw in file:\n        if raw.startswith("#") or not raw.strip():continue\n        s,r,ns,w,d=raw.split();rules[s,int(r)]=ns,int(w),d\n'
        code=before+source+('\n\n# 明确的演示输入与输出\n'+outputs[topic] if topic in outputs else '')
    else:return None
    return {'cells':[{'title':'完整例题 · 已补入口、输入与输出','code':code}],'fixtures':fixtures,'lead':'从知识卡补成完整程序；演示输入已写在代码里，可直接运行并修改。','topics':[topic]}
