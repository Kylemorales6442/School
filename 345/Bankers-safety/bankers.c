#include <stdio.h>
#include <stdbool.h>
#define m 3
#define n 5

int i;
int j;
int available[m] = {10, 5, 7};
int request[m] = {1, 0, 2};
int max[n][m] =
{
    {7, 5, 3},
    {3, 2, 2},
    {9, 0, 2},
    {2, 2, 2},
    {4, 3, 3}
};
int allocation[n][m] =
{
    {0, 1, 0},
    {2, 0, 0},
    {3, 0, 2},
    {2, 1, 1},
    {0, 0, 2}
};
int need[n][m] =
{
    {7, 4, 3},
    {1, 0, 2},
    {6, 0, 0},
    {0, 1, 1},
    {4, 3, 1}
};

int main()
{
    bankers();
}

int bankers()
{
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < m; j++)
        {
            //1. if request <= need, go to step 2 else return error
            if (request[j] <= need[i][j])
            {
                //2. if request <= available then go to step 3 else wait
                if (request[j] <= available[j])
                {
                    //3. temporary updates: 
                    //   available = available - request;
                    available[j] = available[j] - request[j];
                    //   allocation = allocation + request;
                    allocation[i][j] = allocation[i][j] - request[j];
                    //   need = need - request;
                    need[i][j] = need[i][j] - request[j];
                }
                else
                {
                    sleep(0);
                }
            }
            else
            {
                printf("Error: Exceeds Needs");
                return 0;
            }

        }
    }
    //4. check if new state is safe (call safety algorithm)
    safety();
}

bool safety()
{
    bool finish[n][m] = {0};
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < m; j++)
        {
    //1. work = available, finish = false;
            work[j] = available[j];
            finish[i][j] = false;
    //2. find an i such that finish[i] = false and need[i] <= work
    //3. work = work + allocation;
    //   finish[i] = true;
    //   goto step 2
    //4. if finish[i] = true for all i then system is safe
    //   return true
        }
    }
}