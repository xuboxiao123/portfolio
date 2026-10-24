#include "Graph.h"
#include <assert.h>
#include <stdio.h>
int main(void) {
    Graph g=newGraph(5); // vertex 4 initially isolated
    insertEdge(g,(Edge){0,1});insertEdge(g,(Edge){0,2});
    insertEdge(g,(Edge){1,3});insertEdge(g,(Edge){2,3});
    insertEdge(g,(Edge){3,4}); // edge array must grow from capacity 4
    insertEdge(g,(Edge){2,0}); // reverse spelling: duplicate, not a new edge
    assert(numOfEdges(g)==5);
    assert(adjacent(g,0,2)&&adjacent(g,2,0));
    assert(!adjacent(g,0,4));
    assert(!validV(g,-1)&&!validV(g,5)&&!validV(NULL,0));
    puts("Initial graph:");showGraph(g);
    removeEdge(g,(Edge){2,0});removeEdge(g,(Edge){0,2});
    assert(numOfEdges(g)==4&&!adjacent(g,0,2)&&!adjacent(g,2,0));
    puts("After deleting 0 -- 2 twice:");showGraph(g);
    printf("Neighbours of 1:");
    for(int v=0;v<numOfVertices(g);++v)if(adjacent(g,1,v))printf(" %d",v);
    puts("");
    freeGraph(g);g=NULL;
    Graph empty=newGraph(0);assert(numOfVertices(empty)==0);freeGraph(empty);
    puts("PASS: symmetry, duplicate, missing deletion, isolated vertex, empty graph");
    return 0;
}
