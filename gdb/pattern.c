#include<stdio.h>
void printPP(int n){
	  for(int i=1;i<=n;i++){
                for(int j=1;j<=i;j++){
                        printf("*");
                }
                printf("\n");
        }
}
int main(){
	int n;
	printf("enter the lines you want to print");
	scanf("%d",&n);
	printPP(n);
	return 0;
}
