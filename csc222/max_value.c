#include <stdio.h>
int main()
{
  int num1; //initialize num1
  int *p1; // reference pointer 1
  p1 = &num1;
  int num2; //initialize num2
  int *p2; // reference pointer 2
  p2 = &num2;

  printf("Please input an integer value.");
  scanf("%d", &num1);
  printf("Please input another integer value.");
  scanf("%d", &num2);

  if (num1 > num2)
  {
    printf("The first number you entered, %d, is greater.", *p1);
  }
  if (num2 > num1)
  {
    printf("The second number you entered, %d, is greater.", *p2);
  }
  else
  {
    printf("The two numbers you entered are equal.");
  }
}
