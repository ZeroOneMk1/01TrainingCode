#include <stdio.h>

void generateSubsets(int arr[], int n) {
    int totalSubsets = 1 << n;
    int subsetSums[1 << n];
    for(int i = 0; i < 1 << n; i++){
        subsetSums[i] = 0;
    }

    for (int mask = 0; mask < totalSubsets; mask++) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            if (mask & (1 << i)) {
                sum += arr[i];
            }
        }
        subsetSums[mask] = sum;
    }

    int freq[133] = {0}; // Max sum is 132
    for (int i = 0; i < totalSubsets; i++) {
        freq[subsetSums[i]]++;
    }

    printf("Those with a sum of exactly 33 (The sum of the rows) are %d in number\n", freq[33]);

    printf("Sum\tFrequency\n");
    for (int i = 0; i < 133; i++) {
        if (freq[i] > 0) {
            printf("%d\t%d\n", i, freq[i]);
        }
    }

    printf("The most frequent sum is 66 with a frequency of: %d\nThis is exactly the sum of two rows, and half the sum of the entire square!", freq[66]);
}

void generateSubsetsFoursOnly(int arr[], int n) {
    int totalSubsets = 1 << n;
    int freq = 0;

    for (int mask = 0; mask < totalSubsets; mask++) {
        if (__builtin_popcount(mask) == 4) { // Check if the subset size is 4
            int sum = 0;
            for (int i = 0; i < n; i++) {
                if (mask & (1 << i)) {
                    sum += arr[i];
                }
            }
            if (sum == 33) {
                freq++;
            }
        }
    }

    printf("There are %d groupings of 4 that add up to 33\n", freq);
}

int main() {
    int square[] = {1, 14, 14, 4, 11, 7, 6, 9, 8, 10, 10, 5, 13, 2, 3, 15};

    generateSubsetsFoursOnly(square, 16);
    generateSubsets(square, 16);

    return 0;
}