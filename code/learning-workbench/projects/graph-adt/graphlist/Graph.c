#include "Graph.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
static void *checked(void *p) {
    if (p == NULL) { fputs("allocation failed\n", stderr); exit(EXIT_FAILURE); }
    return p;
}
typedef struct Node { Vertex v; struct Node *next; } Node;
struct GraphRep { Node **edges; int nV,nE; };
Graph newGraph(int V) {
    assert(V>=0);Graph g=checked(malloc(sizeof *g));
    g->nV=V;g->nE=0;g->edges=NULL;
    if(V>0) {
        g->edges=checked(malloc((size_t)V*sizeof *g->edges));
        for(int i=0;i<V;++i)g->edges[i]=NULL;
    }
    return g;
}
bool adjacent(Graph g,Vertex x,Vertex y) {
    assert(validV(g,x)&&validV(g,y));
    for(Node *p=g->edges[x];p;p=p->next)if(p->v==y)return true;
    return false;
}
void insertEdge(Graph g,Edge e) {
    assert(validV(g,e.v)&&validV(g,e.w)&&e.v!=e.w);
    if(adjacent(g,e.v,e.w))return;
    Node *a=checked(malloc(sizeof *a)),*b=checked(malloc(sizeof *b));
    *a=(Node){e.w,g->edges[e.v]};*b=(Node){e.v,g->edges[e.w]};
    g->edges[e.v]=a;g->edges[e.w]=b;g->nE++;
}
static void erase(Node **head,Vertex v) {
    // link points to the head slot or a predecessor's next slot.
    Node **link=head;
    while(*link && (*link)->v!=v)link=&(*link)->next;
    if(*link){Node *old=*link;*link=old->next;free(old);}
}
void removeEdge(Graph g,Edge e) {
    assert(validV(g,e.v)&&validV(g,e.w)&&e.v!=e.w);
    if(adjacent(g,e.v,e.w)) {
        erase(&g->edges[e.v],e.w);erase(&g->edges[e.w],e.v);g->nE--;
    }
}
void freeGraph(Graph g) {
    if(!g)return;
    for(int i=0;i<g->nV;++i) {
        Node *p=g->edges[i];
        while(p){Node *next=p->next;free(p);p=next;}
    }
    free(g->edges);free(g);
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
