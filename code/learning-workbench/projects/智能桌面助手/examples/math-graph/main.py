nodes=['sensor','esp32','server','web','phone']
edges={(0,1),(1,2),(2,3),(2,4)}
adj=[set() for _ in nodes]
for u,v in edges:adj[u].add(v);adj[v].add(u)
matrix=[[int(v in adj[u]) for v in range(len(nodes))] for u in range(len(nodes))]
print('邻接表:',list(zip(nodes,adj)));print('矩阵:',matrix)
assert sum(map(len,adj))==2*len(edges)

from collections import deque
queue=deque([0]);parent={0:None}
while queue:
    u=queue.popleft()
    for v in sorted(adj[u]):
        if v not in parent:parent[v]=u;queue.append(v)
path=[];v=4
while v is not None:path.append(nodes[v]);v=parent[v]
print('传感器到手机的路径:',list(reversed(path)))
assert len(parent)==len(nodes)