# include <stdio.h>
# include <stdlib.h> // standard library, includes malloc() and alloc()
int *pointer(void); // declare pointer() function
void main() {
  int *ptr; // declare pointer variable ptr
  ptr = pointer(); // assign pointer() return value to ptr
  *ptr = 42; // dereference ptr and change value to 42
  printf("%d", *ptr); // display pointer value
  }
int *pointer() {
  int *temp = malloc(sizeof(int)); // allocates memory to store the temp pointer, allowing temp to be pointer type
  return (temp); // cant return memory address, so returns pointer to an address instead.
}
