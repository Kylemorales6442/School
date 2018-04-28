#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <pthread.h>

#define n 5

int nextp = 0, nextc = 0; // items pro and cons
int in = 0; // prevent underflow
int out = 0; // prevent overflow
int count = 0;
int terminator = 10; // prevents the code from running for a very long time
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

int produceitem(int i)
{
    int ns = 5;
    time_t t;
    /* Intializes random number generator */
    srand((unsigned) time(&t));
    return(rand() % i*ns);
}

void *producer(void *ptr)
{
    int i = 10;
    char *msg = (char *)ptr;
    printf("msg: %s\n", msg);
    do
    {
        nextp = produceitem(i);
        terminator--;
        i = i+5;
        //keep producing an item until buffer is full
        if((in+1) % n == out){continue;}
        if(count == (n)){printf("Buffer overflow....\n"); sleep(2);continue;}
        printf("produced %d \n", nextp);
        // Start of critical section
        pthread_mutex_lock(&mutex);
        in = (in+1)%n;
        count++;
        // End of critical section
        pthread_mutex_unlock(&mutex);
        printf("P>>in = %d and out=%d\n", in,out);
        sleep(1);
    }while(terminator != 0);
    return 0;
}

void *consumer(void *ptr)
{
    char *msg = (char *)ptr;
    printf("msg: %s\n", msg);
    do{
        //keep consuming until buffer is empty
        if(in==out) {continue;}
        if(count == 0){printf("Buffer underflow....\n");continue;}
        // Start of critical section
        pthread_mutex_lock(&mutex);
        printf("Consumed %d\n", nextc);
        out = (out+1)%n;
        count--;
        // End of critical section
        pthread_mutex_unlock(&mutex);
        printf("C>>in = %d and out=%d\n", in,out);
        sleep (3);
    }while(terminator != 0);
    return 0;
}

int main()
{
    pthread_t pro,cons;
    char *msg1 = "Producer thread";
    char *msg2 = "Consumer thread";
    //Spawn threads
    pthread_create(&pro, NULL, producer, (void*)msg1);
    pthread_create(&cons, NULL, consumer,(void*)msg2);
    pthread_join(pro,NULL);
    pthread_join(cons,NULL);
    return 0;
}