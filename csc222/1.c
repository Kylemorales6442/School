#include <stdio.h>

int main(){

	int arr[5][5];

	for (int row = 0; row < 5; row ++){
		for (int col = 0; col < 5; col ++){
			if (row == col){
				arr[row][col] = (col+1)*(col+1);
			} else {
				arr[row][col] = 0;
			}
		}
	}

	for (int row = 0; row < 5; row ++){
		for (int col = 0; col < 5; col ++){
			printf("%d ",arr[row][col]);
		}
		printf("\n");
	}
}
