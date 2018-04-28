#include <stdio.h>
#include <pthread.h>
#define NUM_LOOPS 500000

long long sum = 0; // a global variable

void* counting_function(void *ptr)
{
    int offset =*(int *) ptr;
    for(int i=0; i<NUM_LOOPS; i++)
    {
        sum=sum+offset;
    }
    pthread_exit(NULL); // return arguments from thread
}
int main(void)
{
    int offset1 = 100;
    pthread_t id1;
    // Declare an object of type thread
    pthread_create(&id1, NULL, counting_function, &offset1);
    // Create a thread using pthread_create with the following
    // arguments
    // First argument -> The thread object id
    // Second argument -> The attributes of the thread
    //(Default = NULL)
    // Third argument -> The function invoked by the thread
    // Fourth argument --> The variable passed into the
    //function executed by the thread (as a pointer)
    pthread_join(id1, NULL); // Joining of thread
    printf("Sum = %lld\n", sum);
    return 0;
}