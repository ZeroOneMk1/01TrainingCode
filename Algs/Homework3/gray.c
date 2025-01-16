#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

void printBinary(int number)
{
    int binary[7] = {0};
    int index = 0;
    int n = 7;

    while (number > 0)
    {
        binary[index] = number % 2;
        number = number / 2;
        index++;
    }

    for (int i = n - 1; i >= 0; i--)
    {
        printf("%d", binary[i]);
    }
}

void brgc(int n)
{

    int size = 1 << n;

    const char *names[] = {"Alfie", "Berty", "Crizz", "Dietz", "Elmer", "Fleek", "Gomer"};

    printf("\n i;GrayCode; Players                                            ; Playing Action\n");

    int grayCode = 0;
    int prevGrayCode = 0;

    char **sequence = (char **)malloc(size * sizeof(char *));
    for (int i = 0; i < size; i++) {
        sequence[i] = (char *)malloc((strlen(names[0]) + 1) * sizeof(char));
    }

    for (int i = 0; i < size; i++)
    {
        prevGrayCode = grayCode;
        grayCode = i ^ (i >> 1);

        printf("%2d; ", i);
        printBinary(grayCode);
        printf("; Players: ");
        for (int j = 0; j < n; j++)
        {
            if ((grayCode >> j) & 1)
            {

                printf("%s ", names[j]);
            }else{
                printf("      ");
            }
        }

        if (i == 0)
        {
            printf("; Silent Stage\n");
        }
        else if (prevGrayCode < grayCode)
        {
            printf("; %s Joining\n", names[(int)log2((double)(grayCode ^ prevGrayCode))]);
            strcpy(sequence[i], names[(int)log2((double)(grayCode ^ prevGrayCode))]);
        }
        else
        {
            printf("; %s Fading Out\n", names[(int)log2((double)(grayCode ^ prevGrayCode))]);
            strcpy(sequence[i], names[(int)log2((double)(grayCode ^ prevGrayCode))]);
        }
    }

    printf("\nThe List of people who switch in/out: \n\n");
    int i = 1;
    for(i = 1; i < (1 << n) - 1; i++){
        printf("%s, ", sequence[i]);
    }
    printf("%s\n\n", sequence[i]);

    for (int i = 0; i < size; i++) {
        free(sequence[i]);
    }
    free(sequence);
}

int main()
{
    brgc(7);

    return 0;
}
