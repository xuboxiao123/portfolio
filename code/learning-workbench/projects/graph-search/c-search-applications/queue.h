#ifndef QUEUE_H
#define QUEUE_H
#include <stdbool.h>
typedef struct QueueRep *queue;
queue newQueue(void);
bool QueueIsEmpty(queue q);
void QueueEnqueue(queue q, int value);
int QueueDequeue(queue q);
void showQueue(queue q);
void dropQueue(queue q);
#endif
