#include "Search.h"
#include <assert.h>
#include <stdio.h>
int main(void) {
    Graph g=newGraph(4);insertEdge(g,(Edge){0,1});insertEdge(g,(Edge){1,2});insertEdge(g,(Edge){2,3});
    assert(hasHamiltonianPath(g,0,3));assert(!hasHamiltonianPath(g,0,2));
    assert(hasEulerPath(g,0,3));assert(!hasEulerPath(g,0,2));freeGraph(g);
    g=newGraph(6);Edge es[]={{0,1},{1,2},{2,0},{3,4},{4,5},{5,3}};
    for(int i=0;i<6;++i)insertEdge(g,es[i]);
    assert(!hasEulerPath(g,0,0)); // all degrees even, but edges are disconnected
    freeGraph(g);g=newGraph(1);assert(hasEulerPath(g,0,0)&&hasHamiltonianPath(g,0,0));freeGraph(g);
    puts("PASS Hamilton/Euler: length, endpoint, connectivity, zero-edge path");return 0;
}
