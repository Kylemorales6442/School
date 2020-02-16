#include <stdio.h>
int main()
{
  printf("Please enter an integer.");
  int n;
  scanf("%d", &n);
  if (n % 2 == 0)
  {
    printf("%d is even.", n);
  }
  else
  {
    printf("%d is odd.", n);
  }
}
