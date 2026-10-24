#include <stdio.h>
void insertion(int *a,int n){for(int i=1;i<n;i++){int key=a[i],j=i-1;while(j>=0&&a[j]>key){a[j+1]=a[j];j--;}a[j+1]=key;}}
int main(void){int a[]={7,2,5,2};int n=(int)(sizeof a/sizeof a[0]);insertion(a,n);for(int i=0;i<n;i++)printf("%d%s",a[i],i+1==n?"\n":" ");return 0;}