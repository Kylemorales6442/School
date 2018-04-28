// CODE 0-2: ForkFun2.c
#include <stdio.h>
#include <stdlib.h> // for exit()
#include <unistd.h>
#include <sys/wait.h> // for wait()

// Print statements in order

int main()
{
    int chid;

    printf("P: Statement 1 \n");

    chid = fork(); // The fork() system call

    if (chid==0){
        printf("C: Statement 3 \n");
        exit(0); // Exiting the child process
    }

    printf("P: Statement 2 \n");
    wait(0); // Parent thread waits for the child to exit
    printf("P: Statement 4 \n");

    return 0;
}