#include <stdio.h>
#include <string.h>
#include <ctype.h>

void preprocessString(char str[]) {
    int len = strlen(str);
    int i, j = 0;

    for (i = 0; i < len; i++) {
        if (isalnum(str[i])) {
            str[j++] = tolower(str[i]);
        }
    }

    str[j] = '\0';
}

int isPalindrome(char str[], int start, int end) {
    if (start >= end) {
        return 1;
    }

    if (str[start] == str[end]) {
        return isPalindrome(str, start + 1, end - 1);
    } else {
        return 0;
    }
}

int main() {
    char input[256];

    printf("Enter a string: ");
    fgets(input, sizeof(input), stdin);

    input[strcspn(input, "\n")] = '\0';

    preprocessString(input);

    if (isPalindrome(input, 0, strlen(input) - 1)) {
        printf("The string is a palindrome!\n");
    } else {
        printf("The string is not a palindrome!\n");
    }

    return 0;
}
