#include "Search.h"
#include <assert.h>
#include <stdio.h>
int main(void) {
    Graph g=newGraph(7);
    Edge es[]={{0,1},{1,2},{3,4},{4,5},{5,3}};
    for(int i=0;i<5;++i)insertEdge(g,es[i]);
    int labels[SEARCH_MAX];assert(components(g,labels)==3);
    assert(hasCycle(g)); // first component is a tree; second contains a cycle
    for(int v=0;v<7;++v)printf("componentOf[%d]=%d\n",v,labels[v]);
    freeGraph(g);
    g=newGraph(2);insertEdge(g,(Edge){0,1});assert(!hasCycle(g));freeGraph(g);
    g=newGraph(0);assert(components(g,labels)==0&&!hasCycle(g));freeGraph(g);
    puts("PASS applications: parent edge, disconnected cycle, isolated vertex, empty graph");return 0;
}
