#include <stdlib.h>
#include <stdio.h>
#include <time.h>

unsigned long long int lucas(int);
unsigned long long int lucas_my(int);
void printLucasSeries(int);
void printLucasSeries_my(int);

int main(){
    int depth;

    printf("How many values do you want?");
    scanf("%d", &depth);

    if (depth < 0) {
        printf("Depth must be a non-negative integer.\n");
    } else {
        printf("Lucas series up to depth %d: ", depth);
        printLucasSeries(depth);
        printLucasSeries_my(depth);
        printf("\n");
        printf("The order of Growth is exponential!\n\n");
    }
    return 0;
}

unsigned long long int lucas(int depth) {
    if (depth == 0) {
        return 2;
    } else if (depth == 1) {
        return 1;
    } else {
        return lucas(depth - 1) + lucas(depth - 2);
    }
}

unsigned long long int lucas_my(int depth) {
    if (depth == 0) {
        return 69;
    } else if (depth == 1) {
        return 420;
    } else {
        return lucas(depth - 1) + lucas(depth - 2);
    }
}

void printLucasSeries(int depth) {
    double times_taken[depth];
    for (int i = 0; i < depth; i++) {
        clock_t start = clock();
        unsigned long long int result = lucas(i);
        clock_t end = clock();
        double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
        times_taken[i] = time_taken;

        printf("Lucas number at position %d is %llu, time taken: %f seconds\n", i, result, time_taken);
        if(i != 0){
            printf("Ratio between this and last attempt: %.2f\n", times_taken[i]/times_taken[i-1]);
        }
    }
}

void printLucasSeries_my(int depth) {
    double times_taken[depth];
    for (int i = 0; i < depth; i++) {
        clock_t start = clock();
        unsigned long long int result = lucas_my(i);
        clock_t end = clock();
        double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
        times_taken[i] = time_taken;

        printf("ALTERED Lucas number at position %d is %llu, time taken: %f seconds\n", i, result, time_taken);
        if(i != 0){
            printf("Ratio between this and last attempt: %.2f\n", times_taken[i]/times_taken[i-1]);
        }
    }
}
