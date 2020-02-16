# include <stdio.h>
void swap(int *x, int *y) { // passing by reference
*x = *x + *y; // x becomes 5 + 7
*y = *x - *y; // can then "swap" values by removing y component
*x = *x - *y; // new x component is combination of x and y, now subtract y
}
int main(){
  int a = 5, b = 7; // variables declaration
  printf("The value of A before swap = %d \n", a);
  printf("The value of B before swap = %d \n", b);
  swap(&a, &b); // calling by reference
  printf("\nThe value of A after swap = %d \n", a);
  printf("The value of B after swap = %d \n", b);
  return 0;
  }
