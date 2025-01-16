#include <stdio.h>
#include <math.h>

int mountain[8][8] = {
    {35, 89, 52, 66, 82, 20, 95, 21},
    {79, 5, 14, 23, 78, 37, 40, 74},
    {32, 59, 17, 25, 31, 4, 16, 63},
    {91, 11, 77, 48, 13, 71, 92, 15},
    {56, 70, 47, 64, 22, 88, 67, 12},
    {83, 97, 94, 27, 65, 51, 30, 7},
    {10, 41, 1, 86, 46, 24, 53, 93},
    {96, 33, 44, 98, 75, 68, 99, 84}};

int partial_solution[8][8] ={
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}};

int track[8] = {-1};

int max(int a, int b) {
    return a > b ? a : b;
}

char* narration[] = {"Starting at", "Then he proceeded to", "After which he stepped on", "Followed by", "Right after which he went to", "After this, he moved to", "Smelling his victory, he hopped on", "Finally finishing at"};

void printMatrix(int matrix[8][8]) {
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int bilbosSuperSmartAlgorithm(int row, int col){
    if(row == 7){
        return mountain[row][col];
    }
    if(col == 0){
        return mountain[row][col] + max(partial_solution[row + 1][col]    , partial_solution[row + 1][col + 1]);
    }else if(col == 7){
        return mountain[row][col] + max(partial_solution[row + 1][col - 1], partial_solution[row + 1][col]);
    }else{
        return mountain[row][col] + max(max(partial_solution[row + 1][col - 1], partial_solution[row + 1][col]), partial_solution[row + 1][col + 1]);
    }
    
}

int findStartingIndex(){
    int ind = 0;
    int max = 0;
    for(int i = 0; i < 8; i++){
        if(partial_solution[0][i] > max){
            max = partial_solution[0][i];
            ind = i;
        }
    }
    return ind;
}

void backtrackForPath(){
    int movingIndex = findStartingIndex();
    track[7] = movingIndex;
    for(int i = 1; i < 8; i++){
        if(movingIndex == 0){
            if(partial_solution[i][movingIndex + 1] > partial_solution[i][movingIndex]){
                movingIndex++;
            }
        }else if(movingIndex == 7){
            if(partial_solution[i][movingIndex - 1] > partial_solution[i][movingIndex]){
                movingIndex--;
            }
        }else{
            if(partial_solution[i][movingIndex + 1] > partial_solution[i][movingIndex]){
                if(partial_solution[i][movingIndex + 1] > partial_solution[i][movingIndex - 1]){
                    movingIndex++;
                }else{
                    movingIndex--;
                }
            }else if(partial_solution[i][movingIndex - 1] > partial_solution[i][movingIndex]){
                movingIndex--;
            }
        }
        track[7-i] = movingIndex;
    }
}

int main(){
    for(int row = 7; row >= 0; row--){
        for(int col = 0; col < 8; col++){
            partial_solution[row][col] = bilbosSuperSmartAlgorithm(row, col);
        }
    }
    printMatrix(partial_solution);
    backtrackForPath();

    printf("\n\nThe Super Smart Path Bilbo found is:\n\n");
    for(int i = 0; i < 8; i++){
        printf("%s the tile in column %d in line with Vault %d\n", narration[i], i+1, track[i]+1);
    }

    printf("\nOn this path, Bilbo collected %d Gems!\n\n", partial_solution[0][track[7]]);

    return 0;
}