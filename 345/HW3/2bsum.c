#include <stdio.h>
#include <pthread.h>
#define NUM_LOOPS 500000

long long sum = 0; // a global variable

void* counting_function(void *ptr)
{
    int offset =*(int *) ptr;
    for(int i=0; i<NUM_LOOPS; i++)
    { sum=sum+offset; }
    pthread_exit(NULL);
}
int main(void)
{
    int offset1 =1;
    int offset2 = -1; // Declare a second offset
    pthread_t id1, id2; // Declare another object of thread
    // Spawn Treads
    pthread_create(&id1, NULL, counting_function, &offset1);
    pthread_create(&id2, NULL, counting_function, &offset2);
    // Create your second thread
    // Join Threads
    pthread_join(id1, NULL);
    pthread_join(id2, NULL); // Join the threads back to main
    printf("Sum = %lld\n", sum);
    return 0;
}