#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int *make_value(void) {
    int *owned=malloc(sizeof *owned);
    if(owned) *owned=7;
    return owned;
}
int main(void) {
    int local=7;
    int *p=malloc(3*sizeof *p);
    if(!p){puts("allocation failed");return 1;}
    p[0]=10;p[1]=20;p[2]=30;
    int *q=p;
    printf("sizeof(int)=%zu, sizeof(pointer)=%zu (this build)\n",sizeof(int),sizeof p);
    printf("address of local = %p\n",(void*)&local);
    printf("address of pointer object &p = %p\n",(void*)&p);
    printf("address stored in p = %p, q = %p\n",(void*)p,(void*)q);
    printf("array element addresses: %p %p %p\n",(void*)&p[0],(void*)&p[1],(void*)&p[2]);
    q[1]=99;
    printf("shared array: %d %d %d\n",p[0],p[1],p[2]);
    uint32_t number=UINT32_C(0x12345678);
    const unsigned char *bytes=(const unsigned char*)&number;
    printf("object bytes, increasing addresses:");
    for(size_t i=0;i<sizeof number;i++)printf(" %02X",bytes[i]);
    puts("\nByte order is measured here, not assumed for every machine.");
    free(p);
    /* Do not evaluate dangling pointers: overwrite both pointer objects. */
    p=NULL;q=NULL;
    int *owned=make_value();
    if(!owned)return 1;
    printf("allocated object outlives helper call: %d\n",*owned);
    free(owned);owned=NULL;
    puts("These are process addresses, not measured DRAM physical addresses.");
    return 0;
}
