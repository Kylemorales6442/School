#include <stdio.h>

int main(){
	
	int arr[5][5];
	int num = 5;
	
	for (int r = 0; r < 5; r ++){
		for (int c = 0; c < 5; c ++){
			if (r + c == 4){
				arr[r][c] = num;
				num = num * 2;
			} else {
				arr[r][c] = 0;
			}
		}
	}
	
	for (int r = 0; r < 5; r ++){
		for (int c = 0; c < 5; c ++){
			printf("%d ",arr[r][c]);
		}
		printf("\n");
	}
	
}

