#ifndef SEARCH_H
#define SEARCH_H
#include "Graph.h"
#define SEARCH_MAX 64
extern int visited[SEARCH_MAX]; // -1 = undiscovered; otherwise PREDECESSOR
bool hasPath(Graph g, Vertex src, Vertex dest);
bool findPathDFS(Graph g, Vertex src, Vertex dest);
bool findPathBFS(Graph g, Vertex src, Vertex dest);
void displayPath(Graph g, Vertex src, Vertex dest);
bool hasCycle(Graph g);
int components(Graph g, int componentOf[SEARCH_MAX]);
bool hasHamiltonianPath(Graph g, Vertex src, Vertex dest);
bool hasEulerPath(Graph g, Vertex src, Vertex dest);
#endif
