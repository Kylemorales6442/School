#include <stdio.h>
#define NUM_LOOPS 500000

long long sum = 0;

void counting_function(void *ptr) //passing a pointer to fn
{
    int offset =*(int *) ptr;
    // dereferencing a pointer var
    for(int i=0; i<NUM_LOOPS; i++)
    {
        sum=sum+offset;
    }
}
int main(void)
{
    int offset1 =100;
    // creating a variable to be passed to fn
    counting_function(&offset1);// passing address of variable
    printf("Sum = %lld\n", sum);
    return 0;
}