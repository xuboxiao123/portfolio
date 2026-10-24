#include "queue.h"
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
typedef struct Node { int value; struct Node *next; } Node;
struct QueueRep { Node *head, *tail; };
static void *allocate(size_t size) {
    void *p=malloc(size);if(!p){fputs("allocation failed\n",stderr);exit(EXIT_FAILURE);}return p;
}
queue newQueue(void) { queue q=allocate(sizeof *q);q->head=q->tail=NULL;return q; }
bool QueueIsEmpty(queue q) { assert(q);return q->head==NULL; }
void QueueEnqueue(queue q,int value) {
    assert(q);Node *n=allocate(sizeof *n);*n=(Node){value,NULL};
    if(q->tail)q->tail->next=n;else q->head=n;
    q->tail=n;
}
int QueueDequeue(queue q) {
    assert(!QueueIsEmpty(q));Node *n=q->head;int value=n->value;
    q->head=n->next;if(!q->head)q->tail=NULL;free(n);return value;
}
void showQueue(queue q) {
    fputs("queue(front -> back):",stdout);
    for(Node *n=q->head;n;n=n->next)printf(" %d",n->value);
    puts("");
}
void dropQueue(queue q) {
    if(!q)return;
    while(!QueueIsEmpty(q))QueueDequeue(q);
    free(q);
}
