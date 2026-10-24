#include "Search.h"
#include "queue.h"
#include <assert.h>
#include <stdio.h>
int visited[SEARCH_MAX];
static bool seen[SEARCH_MAX];
static void check(Graph g,Vertex src,Vertex dest) {
    assert(numOfVertices(g)<=SEARCH_MAX && validV(g,src) && validV(g,dest));
}
static bool dfsBoolean(Graph g,Vertex v,Vertex dest,int depth) {
    seen[v]=true;
    printf("%*sENTER %d; seen[%d]=true\n",depth*2,"",v,v);
    if(v==dest){printf("%*sRETURN true: target %d\n",depth*2,"",v);return true;}
    for(Vertex w=0;w<numOfVertices(g);++w) {
        if(adjacent(g,v,w)&&!seen[w]) {
            printf("%*sTRY %d -> %d\n",depth*2,"",v,w);
            if(dfsBoolean(g,w,dest,depth+1)) {
                printf("%*sRETURN true: via %d\n",depth*2,"",w);return true;
            }
            printf("%*sRESUME %d: branch %d failed, continue loop\n",depth*2,"",v,w);
        }
    }
    printf("%*sRETURN false: no unused route from %d\n",depth*2,"",v);
    return false;
}
bool hasPath(Graph g,Vertex src,Vertex dest) {
    check(g,src,dest);
    for(int v=0;v<numOfVertices(g);++v)seen[v]=false;
    return dfsBoolean(g,src,dest,0);
}
static void initialise(Graph g,Vertex src) {
    for(int v=0;v<numOfVertices(g);++v)visited[v]=-1;
    visited[src]=src;
}
static bool dfsPredecessor(Graph g,Vertex v,Vertex dest,int depth) {
    printf("%*sENTER %d\n",depth*2,"",v);
    if(v==dest)return true;
    for(Vertex w=0;w<numOfVertices(g);++w) {
        if(adjacent(g,v,w)&&visited[w]==-1) {
            visited[w]=v; // record parent BEFORE entering child
            printf("%*svisited[%d]=%d\n",depth*2,"",w,v);
            if(dfsPredecessor(g,w,dest,depth+1))return true;
            printf("%*sBACKTRACK from %d to %d; keep visited mark\n",depth*2,"",w,v);
        }
    }
    return false;
}
bool findPathDFS(Graph g,Vertex src,Vertex dest) {
    check(g,src,dest);initialise(g,src);return dfsPredecessor(g,src,dest,0);
}
bool findPathBFS(Graph g,Vertex src,Vertex dest) {
    check(g,src,dest);initialise(g,src);
    queue q=newQueue();QueueEnqueue(q,src);showQueue(q);
    while(!QueueIsEmpty(q)) {
        Vertex v=QueueDequeue(q);printf("DEQUEUE %d\n",v);
        if(v==dest){dropQueue(q);return true;}
        for(Vertex w=0;w<numOfVertices(g);++w) {
            if(adjacent(g,v,w)&&visited[w]==-1) {
                visited[w]=v; // discovery mark accompanies enqueue, not dequeue
                QueueEnqueue(q,w);printf("ENQUEUE %d; visited[%d]=%d\n",w,w,v);showQueue(q);
            }
        }
    }
    dropQueue(q);return false;
}
void displayPath(Graph g,Vertex src,Vertex dest) {
    check(g,src,dest);
    if(visited[dest]==-1){puts("no path");return;}
    int route[SEARCH_MAX],length=0;Vertex v=dest;
    while(v!=src) {
        assert(length<numOfVertices(g));route[length++]=v;v=visited[v];assert(validV(g,v));
    }
    route[length++]=src;
    fputs("reverse (dest -> src):",stdout);
    for(int i=0;i<length;++i)printf(" %d",route[i]);puts("");
    fputs("forward (src -> dest):",stdout);
    for(int i=length-1;i>=0;--i)printf(" %d",route[i]);puts("");
}
static bool cycleDFS(Graph g,Vertex v,Vertex parent) {
    seen[v]=true;
    for(Vertex w=0;w<numOfVertices(g);++w)if(adjacent(g,v,w)) {
        if(w==parent)continue; // undirected parent edge is not a new cycle
        if(seen[w]||cycleDFS(g,w,v))return true;
    }
    return false;
}
bool hasCycle(Graph g) {
    assert(numOfVertices(g)<=SEARCH_MAX);
    for(int v=0;v<numOfVertices(g);++v)seen[v]=false;
    for(Vertex v=0;v<numOfVertices(g);++v)if(!seen[v]&&cycleDFS(g,v,-1))return true;
    return false;
}
static void labelDFS(Graph g,Vertex v,int id,int labels[]) {
    labels[v]=id;
    for(Vertex w=0;w<numOfVertices(g);++w)
        if(adjacent(g,v,w)&&labels[w]==-1)labelDFS(g,w,id,labels);
}
int components(Graph g,int labels[SEARCH_MAX]) {
    assert(numOfVertices(g)<=SEARCH_MAX);
    for(int v=0;v<numOfVertices(g);++v)labels[v]=-1;
    int count=0;
    for(Vertex v=0;v<numOfVertices(g);++v)if(labels[v]==-1)labelDFS(g,v,count++,labels);
    return count;
}
static bool hamiltonDFS(Graph g,Vertex v,Vertex dest,int remaining) {
    if(v==dest)return remaining==0;
    seen[v]=true;
    for(Vertex w=0;w<numOfVertices(g);++w)
        if(adjacent(g,v,w)&&!seen[w]&&hamiltonDFS(g,w,dest,remaining-1))return true;
    seen[v]=false; // this search explores other candidate paths
    return false;
}
bool hasHamiltonianPath(Graph g,Vertex src,Vertex dest) {
    check(g,src,dest);
    for(int v=0;v<numOfVertices(g);++v)seen[v]=false;
    return hamiltonDFS(g,src,dest,numOfVertices(g)-1);
}
static void reachableDFS(Graph g,Vertex v) {
    seen[v]=true;
    for(Vertex w=0;w<numOfVertices(g);++w)if(adjacent(g,v,w)&&!seen[w])reachableDFS(g,w);
}
bool hasEulerPath(Graph g,Vertex src,Vertex dest) {
    check(g,src,dest);int degree[SEARCH_MAX]={0};
    if(numOfEdges(g)==0)return src==dest; // allow a zero-edge path
    for(Vertex v=0;v<numOfVertices(g);++v) {
        seen[v]=false;
        for(Vertex w=0;w<numOfVertices(g);++w)if(adjacent(g,v,w))degree[v]++;
    }
    if(degree[src]==0||degree[dest]==0)return false;
    reachableDFS(g,src);
    for(Vertex v=0;v<numOfVertices(g);++v) {
        if(degree[v]>0&&!seen[v])return false; // connectivity cannot be skipped
        bool shouldBeOdd=src!=dest&&(v==src||v==dest);
        if((degree[v]%2!=0)!=shouldBeOdd)return false;
    }
    return true;
}
