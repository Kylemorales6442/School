// CODE 0-2: ForkFun2.c
#include <stdio.h>
#include <stdlib.h> // for exit()
#include <unistd.h>
#include <sys/wait.h> // for wait()

// Print statements in order

int main()
{
    int chid;

    chid = vfork(); // The vfork() system call

    if (chid==0){
        printf("Statement 1 \n");
        exit(0); // Exiting the child process
    }
    
    printf("Statement 2 \n");
    wait(0); // Parent thread waits for the child to exit
    printf("Statement 3 \n");
    printf("Statement 4 \n");

    return 0;
}