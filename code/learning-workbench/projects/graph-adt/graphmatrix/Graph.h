#ifndef GRAPH_H
#define GRAPH_H
#include <stdbool.h>
typedef struct GraphRep *Graph;
typedef int Vertex;
typedef struct Edge { Vertex v, w; } Edge;
Graph newGraph(int V);
bool validV(Graph g, Vertex v);
int numOfVertices(Graph g);
int numOfEdges(Graph g);
void insertEdge(Graph g, Edge e);
void removeEdge(Graph g, Edge e);
bool adjacent(Graph g, Vertex x, Vertex y);
void showGraph(Graph g);
void freeGraph(Graph g);
#endif
