//CODE 0-1: ForkFun1.c
# include <stdio.h>
# include <unistd.h>
int main(int argc, char *argv[])
{
    int chid, count1=0, count2=0;
    printf("Before it forks !\n");
    sleep(10);
    chid = fork(); /* The fork()system call will return a zero if the
    child process is created successfully. A negative number if the child
    process is not created. */
    if (chid==0)
    {
        printf("This is a child process \n");
        while (count1 < 20)
        {
            printf("Child Process: %d\n", count1);
            sleep(1);
            count1++;
        }
    } else {
        printf("This is the parent process\n");
        while(count2 < 20)
        {
            printf("Parent Process: %d\n", count2);
            sleep(1);
            count2++;
        }
    }
    return 0;
}