#include <stdio.h>
#include <stdlib.h>

long long int merge(int arr[], int l, int m, int r)
{
    long long int inversions = 0;

    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    int L[n1], R[n2];

    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    i = 0;
    j = 0;
    k = l;

    while (i < n1 && j < n2)
    {
        if (L[i] <= R[j])
        {
            arr[k] = L[i];
            i++;
        }
        else
        {
            arr[k] = R[j];
            j++;

            inversions += n1 - i;
        }
        k++;
    }

    while (i < n1)
    {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2)
    {
        arr[k] = R[j];
        j++;
        k++;
    }

    return inversions;
}

long long int mergeSort(int arr[], int l, int r)
{
    long long int inversions = 0;

    if (l < r)
    {

        int m = l + (r - l) / 2;

        inversions += mergeSort(arr, l, m);
        inversions += mergeSort(arr, m + 1, r);

        inversions += merge(arr, l, m, r);
    }

    return inversions;
}

void printArray(int A[], int size)
{
    for (int i = 0; i < size; i++)
        printf("%d ", A[i]);
    printf("\n");
}

int main()
{
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
    long long int inversions = mergeSort(numbers, 0, len - 1);

    printf("Number of inversions: %lld\n", inversions);

    return 0;
}
