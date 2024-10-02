#include<stdio.h>

struct ABC{ 
    float a,c;
    int *b;
};

int main(){
    struct ABC ab;
    printf("%ld",sizeof(ab));
}