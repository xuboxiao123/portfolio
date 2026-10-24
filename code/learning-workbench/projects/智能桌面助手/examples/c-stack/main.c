#include <stdio.h>
#include <stdbool.h>
#define CAP 8
typedef struct { int items[CAP]; int size; } Stack;
bool push(Stack *s,int x){if(s->size==CAP)return false;s->items[s->size++]=x;return true;}
bool pop(Stack *s,int *x){if(s->size==0)return false;*x=s->items[--s->size];return true;}
int main(void){Stack s={.size=0};int x;push(&s,2);push(&s,5);push(&s,8);while(pop(&s,&x))printf("%d\n",x);return 0;}