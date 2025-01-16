#include <stdio.h>
#include <stdlib.h>

int first_run;

// Function to print the board
void printBoard(int board[], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (board[i] == j + 1) {
                printf("Q ");
            } else if (board[i] == 0) {
                printf("_ ");
            } else {
                printf(". ");
            }
        }
        printf("\n");
    }
    printf("\n");
}

void printBoardConcise(int board[], int n) {
    printf("%d: [", n);
    int i = 0;
    for (i = 0; i < n-1; i++) {
        printf("%d, ", board[i]);
    }
    printf("%d", board[i]);
    printf("]\n");
}

int removeQueen(int board[], int n, int index){
    if(index < n){
        int retval = board[index];
        board[index] = 0;
        return retval;
    }
    return -1;
}

int lastQueenIndex(int board[], int n){
    for(int i = 0; i < n; i++){
        if(board[i] == 0){
            return i-1;
        }
    }
    return n-1;
}

// Function to check for legal position
int isLegalPosition(int board[], int n) {
    // Check for horizontal conflicts
    for (int i = 0; i < n; i++) {
        if (board[i] != 0) {
            for (int j = i + 1; j < n; j++) {
                if (board[j] != 0 && board[i] == board[j]) {
                    return 0;
                }
            }
        }
    }

    // Check for diagonal conflicts
    for (int i = 0; i < n; i++) {
        if (board[i] != 0) {
            for (int j = 0; j < n; j++) {
                if (i != j && board[j] != 0 && abs(i - j) == abs(board[i] - board[j])) {
                    return 0;
                }
            }
        }
    }

    return 1;
}

void nextPosition(int board[], int n){
    int lqi = lastQueenIndex(board, n) ;
    int lqv = 0; // Last Queen Value
    switch(lqi){
        case -1:
            lqi = 0;
            break;
        default:
            if(isLegalPosition(board, n)){
                if(lqi != n-1){
                    lqv = 0;
                    lqi++;
                }else{
                    lqv = board[lqi];
                }
            }else{
                lqv = board[lqi];
            }
            break;
    }
    if(lqv < n){
        board[lqi] = lqv + 1;
    }else{
        while(lqi >= 0 && board[lqi] == n){
            board[lqi] = 0;
            lqi--;
        }
        if(lqi >= 0){
            board[lqi]++;
        }
    }
}

int nextLegalPosition(int board[], int n){
    nextPosition(board, n);
    while(!isLegalPosition(board, n)){
        nextPosition(board, n);
    }
    if(!first_run && board[0] == 0){
        return 0;
    }else{
        first_run = 0;
        return 1;
    }
}

int main() {

    printf("Boards:\n");
    // All solutions from 4-14
    for(int n = 4; n <= 14; n++){
        first_run = 1;
        int board[n];
        for(int i = 0; i < n; i++){
            board[i] = 0;
        }
        while(nextLegalPosition(board, n)){
            if(board[n-1] != 0){
                printBoardConcise(board, n);
                break;
            }
        }
    }

    printf("\n\nCounts:\n");
    // All solution counts from 4-12
    for(int n = 4; n <= 12; n++){
        first_run = 1;
        int count = 0;
        int board[n];
        for(int i = 0; i < n; i++){
            board[i] = 0;
        }
        while(nextLegalPosition(board, n)){
            if(board[n-1] != 0){
                count++;
            }
        }
        printf("There are %d solutions to the %d-Queens Problem\n", count, n);
    }

    // printBoard(board, n);

    // while(nextLegalPosition(board, n)){
    //     printBoard(board, n);
    // }
    // ABOVE VERSION PRINTS EVERY LEGAL POSITION.

    // int n = 32;
    // first_run = 1;
    // int board[n];
    // for(int i = 0; i < n; i++){
    //     board[i] = 0;
    // }
    // while(nextLegalPosition(board, n)){
    //     if(board[n-1] != 0){
    //         printBoardConcise(board, n);
    //         break;
    //     }
    // }

    // int n = 36;
    // first_run = 1;
    // int board[n];
    // for(int i = 0; i < n; i++){
    //     board[i] = 0;
    // }
    // while(nextLegalPosition(board, n)){
    //     if(board[n-1] != 0){
    //         printBoardConcise(board, n);
    //         break;
    //     }
    // }

    // int n = 15;
    // first_run = 1;
    // int count = 0;
    // int board[n];
    // for(int i = 0; i < n; i++){
    //     board[i] = 0;
    // }
    // while(nextLegalPosition(board, n)){
    //     if(board[n-1] != 0){
    //         count++;
    //     }
    // }
    // printf("There are %d solutions to the %d-Queens Problem\n", count, n);

    // int n = 17;
    // first_run = 1;
    // count = 0;
    // int board[n];
    // for(int i = 0; i < n; i++){
    //     board[i] = 0;
    // }
    // while(nextLegalPosition(board, n)){
    //     if(board[n-1] != 0){
    //         count++;
    //     }
    // }
    // printf("There are %d solutions to the %d-Queens Problem\n", count, n);

    return 0;
}
