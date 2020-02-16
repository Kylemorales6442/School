#include<stdio.h>
void increase(int *a, int *b); // function declaration
void main()
{
 int m = 22, n = 44; // variables declaration
printf("\nInitial values: m = %d and n = %d\n", m, n);
increase(&m, &n); // function invocation
printf("\nValues after increase: m = %d and n = %d\n", m, n);
}
void increase(int *a, int *b) // function definition
{
 *a += 1;
 *b += 1;
}
