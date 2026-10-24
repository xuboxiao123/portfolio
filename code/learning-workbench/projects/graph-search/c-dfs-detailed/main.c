#include "Search.h"
#include <assert.h>
#include <stdio.h>
int main(void) {
    Graph g=newGraph(7); // teaching graph: dead branch + reachable target + isolated 6
    Edge es[]={{0,1},{1,3},{0,2},{2,4},{4,5}};
    for(int i=0;i<5;++i)insertEdge(g,es[i]);
    puts("BOOLEAN DFS 0 -> 5:");assert(hasPath(g,0,5));
    puts("PREDECESSOR DFS 0 -> 5:");assert(findPathDFS(g,0,5));displayPath(g,0,5);
    assert(visited[5]==4&&visited[4]==2&&visited[2]==0);
    assert(!hasPath(g,0,6)); // unreachable target
    assert(hasPath(g,0,0)); // zero-edge path
    assert(findPathDFS(g,0,5)); // independent query resets all markers
    displayPath(g,0,5);freeGraph(g);puts("PASS DFS: backtrack, parent, unreachable, same vertex, reset");
    return 0;
}
