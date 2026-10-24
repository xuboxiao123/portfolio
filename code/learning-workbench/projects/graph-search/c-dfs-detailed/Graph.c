#include "Graph.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
static void *checked(void *p) {
    if (p == NULL) { fputs("allocation failed\n", stderr); exit(EXIT_FAILURE); }
    return p;
}
// Private representation: client code cannot see these fields.
struct GraphRep { int **edges; int nV, nE; };
Graph newGraph(int V) {
    assert(V >= 0);
    Graph g = checked(malloc(sizeof *g));
    g->nV=V; g->nE=0; g->edges=NULL;
    if (V == 0) return g; // avoid depending on malloc(0)
    g->edges=checked(malloc((size_t)V * sizeof *g->edges));
    for (int i=0; i<V; ++i)
        g->edges[i]=checked(calloc((size_t)V, sizeof *g->edges[i]));
    return g;
}
bool adjacent(Graph g, Vertex x, Vertex y) {
    assert(validV(g,x) && validV(g,y));
    return g->edges[x][y] != 0;
}
void insertEdge(Graph g, Edge e) {
    assert(validV(g,e.v) && validV(g,e.w) && e.v != e.w);
    if (!adjacent(g,e.v,e.w)) {
        g->edges[e.v][e.w]=1; g->edges[e.w][e.v]=1;
        g->nE++; // two symmetric cells, ONE undirected edge
    }
}
void removeEdge(Graph g, Edge e) {
    assert(validV(g,e.v) && validV(g,e.w) && e.v != e.w);
    if (adjacent(g,e.v,e.w)) {
        g->edges[e.v][e.w]=0; g->edges[e.w][e.v]=0;
        g->nE--;
    }
}
void freeGraph(Graph g) {
    if (!g) return;
    for (int i=0; i<g->nV; ++i) free(g->edges[i]);
    free(g->edges); free(g);
}
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
