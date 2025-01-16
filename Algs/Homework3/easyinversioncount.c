#include <stdio.h>

int easy_inversion_count(int* arr, int arrlength){
    int count = 0;
    for(int i = 0; i < arrlength; i++){
        for(int j = i + 1; j < arrlength; j++){
            if(arr[i] > arr[j]){
                count++;
            }
        }
    }
    return count;
}

int main() {
    int len;

    printf("Enter the length of the array: ");
    scanf("%d", &len);

    if (len <= 0) {
        printf("Invalid array length. Please enter a positive integer.\n");
        return 1;
    }

    int numbers[len];

    printf("Enter %d numbers separated by spaces: ", len);
    for (int i = 0; i < len; i++) {
        scanf("%d", &numbers[i]);
    }

    printf("Entered array: ");
    for (int i = 0; i < len; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    int invs = easy_inversion_count(numbers, len);
    printf("There are %d inversions!\n", invs);

    return 0;
}
