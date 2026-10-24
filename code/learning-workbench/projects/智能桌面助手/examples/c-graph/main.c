#include <stdio.h>
#define V 5
int main(void){int m[V][V]={{0}},edges[][2]={{0,1},{0,2},{1,3},{2,3},{3,4}};for(int i=0;i<5;i++){int u=edges[i][0],v=edges[i][1];m[u][v]=m[v][u]=1;}int q[V],head=0,tail=0,seen[V]={0};seen[0]=1;q[tail++]=0;while(head<tail){int u=q[head++];printf("%d ",u);for(int v=0;v<V;v++)if(m[u][v]&&!seen[v]){seen[v]=1;q[tail++]=v;}}puts("");return 0;}