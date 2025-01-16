#include <stdio.h>
#include <math.h>

void printMatrix(int n, double A[n][n+1]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= n; j++) {
            printf("%.2f\t", A[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

int gaussJordanElimination(int n, double A[n][n+1]) {
    for (int i = 0; i < n; i++) {
        int pivotRow = i;
        for (int j = i + 1; j < n; j++) {
            if (fabs(A[j][i]) > fabs(A[pivotRow][i])) {
                pivotRow = j;
            }
        }

        for (int k = i; k <= n; k++) {
            double temp = A[i][k];
            A[i][k] = A[pivotRow][k];
            A[pivotRow][k] = temp;
        }


        if (fabs(A[i][i]) < 1e-10) {
            return 0; // The system is not solvable! (Redundant)
        }

        double pivot = A[i][i];
        for (int k = i; k <= n; k++) {
            A[i][k] /= pivot;
        }


        for (int j = 0; j < n; j++) {
            if (j != i) {
                double factor = A[j][i];
                for (int k = i; k <= n; k++) {
                    A[j][k] -= factor * A[i][k];
                }
            }
        }
    }
    return 1;  // The system is solvable
}

int main() {
    int n = 9;
    double A[9][10] = {{1, 1, 1, 1, 1, 1, 1, 1, 1, 122},
                          {1, 1, 1, 1, 1, -1, -1, -1, -1, -88},
                          {1, -1, 1, -1, 1, -1, 1, -1, 1, 32},
                          {1, 1, 0, 0, 0, 0, 0, 0, 0, 3},
                          {0, 0, 1, 1, 0, 0, 0, 0, 0, 7},
                          {0, 0, 0, 0, 1, 1, 0, 0, 0, 18},
                          {0, 0, 0, 0, 0, 0, 0, 1, 1, 76},
                          {9, -8, 7, -6, 5, -4, 3, -2, 1, 41},
                          {1, 1, -1, 1, 1, -1, 1, 1, -1, 0}};

    // Redundancy check
    if (n + 1 != sizeof(A[0]) / sizeof(A[0][0])) {
        printf("Error: System is overdetermined or underdetermined.\n");
        return 1;
    }

    printf("Original System:\n");
    printMatrix(n, A);

    if (gaussJordanElimination(n, A)) {
        printf("After Gauss-Jordan Elimination:\n");
        printMatrix(n, A);

        printf("Solution:\n");
        for (int i = 0; i < n; i++) {
            printf("x%d = %.0f\n", i+1, A[i][n]);
        }
    } else {
        printf("The system is not solvable.\n");
    }

    return 0;
}