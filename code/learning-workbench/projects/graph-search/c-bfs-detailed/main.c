#include "Search.h"
#include <assert.h>
#include <stdio.h>
int main(void) {
    Graph g=newGraph(10);
    // Same graph data as the course Programs/bfsQueue.c (not assumed identical to every slide figure).
    Edge es[]={{0,1},{0,2},{0,5},{1,5},{2,3},{3,4},{3,5},{3,8},{4,5},{4,7},{4,8},{5,6},{7,8},{7,9},{8,9}};
    for(int i=0;i<15;++i)insertEdge(g,es[i]);
    assert(findPathBFS(g,0,6));displayPath(g,0,6);
    assert(visited[6]==5&&visited[5]==0); // 0 -> 5 -> 6
    assert(findPathBFS(g,0,0));displayPath(g,0,0);
    freeGraph(g);
    g=newGraph(3);insertEdge(g,(Edge){0,1});assert(!findPathBFS(g,0,2));freeGraph(g);
    puts("PASS BFS: shortest edge count, cycle, same vertex, unreachable");return 0;
}
