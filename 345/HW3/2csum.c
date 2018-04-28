#include <stdio.h>
#include <pthread.h>
#define NUM_LOOPS 500000

long long sum = 0; // a global variable

pthread_mutex_t mutex=PTHREAD_MUTEX_INITIALIZER;
void* counting_function(void *ptr)
{
    int offset =*(int *) ptr;
    for(int i=0; i<NUM_LOOPS; i++)
    {
        // Start of crtical section
        pthread_mutex_lock(&mutex);
        sum=sum+offset;
        // End of critical section
        pthread_mutex_unlock(&mutex);
    }
    pthread_exit(NULL); // passing return arguments from thread
}
int main(void)
{
    int offset1 =1;
    int offset2 = -1;
    pthread_t id1, id2;
    // Spawn Threads
    pthread_create(&id1, NULL, counting_function, &offset1);
    pthread_create(&id2, NULL, counting_function, &offset2);
    // Join Threads
    pthread_join(id1, NULL);
    pthread_join(id2, NULL);
    printf("Sum = %lld\n", sum);
    return 0;
}