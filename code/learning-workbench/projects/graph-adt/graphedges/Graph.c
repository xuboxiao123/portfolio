#include "Graph.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
static void *checked(void *p) {
    if (p == NULL) { fputs("allocation failed\n", stderr); exit(EXIT_FAILURE); }
    return p;
}
struct GraphRep { Edge *edges; int nV,nE,capacity; };
Graph newGraph(int V) {
    assert(V>=0);
    Graph g=checked(malloc(sizeof *g));
    g->nV=V;g->nE=0;g->capacity=4;
    g->edges=checked(malloc((size_t)g->capacity*sizeof *g->edges));
    return g;
}
static int findEdge(Graph g,Vertex x,Vertex y) {
    for(int i=0;i<g->nE;++i) {
        Edge e=g->edges[i];
        if((e.v==x&&e.w==y)||(e.v==y&&e.w==x))return i;
    }
    return -1;
}
bool adjacent(Graph g,Vertex x,Vertex y) {
    assert(validV(g,x)&&validV(g,y));return findEdge(g,x,y)>=0;
}
void insertEdge(Graph g,Edge e) {
    assert(validV(g,e.v)&&validV(g,e.w)&&e.v!=e.w);
    if(findEdge(g,e.v,e.w)>=0)return;
    if(g->nE==g->capacity) {
        // Teaching inputs are small; check integer-size limits for huge graphs.
        int next=g->capacity*2;
        Edge *larger=checked(realloc(g->edges,(size_t)next*sizeof *larger));
        g->edges=larger;g->capacity=next;
    }
    g->edges[g->nE++]=e;
}
void removeEdge(Graph g,Edge e) {
    assert(validV(g,e.v)&&validV(g,e.w)&&e.v!=e.w);
    int i=findEdge(g,e.v,e.w);
    if(i>=0)g->edges[i]=g->edges[--g->nE];
}
void freeGraph(Graph g) { if(g){free(g->edges);free(g);} }
bool validV(Graph g, Vertex v) { return g != NULL && v >= 0 && v < g->nV; }
int numOfVertices(Graph g) { assert(g); return g->nV; }
int numOfEdges(Graph g) { assert(g); return g->nE; }
void showGraph(Graph g) {
    assert(g);
    printf("V=%d E=%d\n", g->nV, g->nE);
    for (Vertex v=0; v<g->nV; ++v)
        for (Vertex w=v+1; w<g->nV; ++w)
            if (adjacent(g,v,w)) printf("%d -- %d\n",v,w);
}
