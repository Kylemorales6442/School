#include <stdio.h>

int main(){

	int arr[5][5];
	int num = 5;

	for (int row = 0; row < 5; row ++){
		for (int col = 0; col < 5; col ++){
			if (row + col == 4){
				arr[row][col] = num;
				num = num * 2;
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
