#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_FILENAME_LENGTH 256

typedef struct {
    int hashAddress;
    char* hashedWord;
    int hashValue;
} HashEntry;

void displayTable(HashEntry* table, int size);

void initializeTable(HashEntry** table, int size) {
    *table = (HashEntry*)malloc(size * sizeof(HashEntry));
    for (int i = 0; i < size; i++) {
        (*table)[i].hashAddress = -1; // -1 indicates an empty slot
        (*table)[i].hashedWord = NULL;
        (*table)[i].hashValue = -1;
    }
}

int hash(char* word, int wordLength, int tableSize) {
    long int hashValue = 0;
    for (int i = 0; i < wordLength; i++) {
        hashValue = (hashValue * 123 + word[i]) % tableSize;
    }
    printf("hashValue: %ld\n", hashValue);
    printf("Word: %s\n", word);
    hashValue = hashValue % tableSize;
    return hashValue;
}

void insertIntoTable(HashEntry* table, int hashAddress, char* word, int hashValue, int tableSize) {
    int i = hashAddress;
    int initialIndex = i;
    int onInitial = 1;

    // displayTable(table, TABLE_SIZE);

    printf("I IS: %d\n", i);
    while (table[i].hashAddress != -1 && (i != initialIndex || onInitial)) {
        if (strcmp(table[i].hashedWord, word) == 0) {
            return;
        }
        i = (i + 1) % tableSize;
        onInitial = 0;
    }

    if (i == initialIndex && !onInitial) {
        fprintf(stderr, "Error: Hash table is full\n");

        displayTable(table, tableSize);

        exit(1);
    }

    table[i].hashedWord = strdup(word);

    if (table[i].hashedWord == NULL) {
        fprintf(stderr, "Error: Memory allocation failed\n");
        exit(1);
    }

    table[i].hashAddress = hashAddress;
    table[i].hashValue = hashValue;
}

void removePeriodsAndCommas(char *input, char *output) {
    int inputLength = strlen(input);
    int outputIndex = 0;

    for (int i = 0; i < inputLength; i++) {
        if (input[i] != '.' && input[i] != ',' && input[i] != ';' && input[i] != ':' && input[i] != '!' && input[i] != '?' && input[i] > 0) {
            output[outputIndex++] = input[i];
        }
    }

    // Null-terminate the output string
    output[outputIndex] = '\0';
}

void displayTable(HashEntry* table, int size) {
    printf("Displaying table:\n");
    for (int i = 0; i < size; i++) {
        if (table[i].hashAddress != -1) {
            printf("Hash Address: %d, Hashed Word: %s, Hash Value: %d\n",
                   i, table[i].hashedWord, table[i].hashValue);
        }
        else{
            printf("Hash Address: %d, Hashed Word: %s, Hash Value: %d\n",
                   i, table[i].hashedWord, table[i].hashValue);
        }
    }
}

void calculateLoadFactor(HashEntry* table, int size) {
    int nonEmptyAddresses = 0;

    for (int i = 0; i < size; i++) {
        if (table[i].hashAddress != -1) {
            nonEmptyAddresses++;
        }
    }

    float loadFactor = (float)nonEmptyAddresses / size;

    printf("Number of non-empty addresses: %d\n", nonEmptyAddresses);
    printf("Load Factor (α): %.2f\n", loadFactor);
}

void findLongestEmptyArea(HashEntry* table, int size) {
    int longestEmptyArea = 0;
    int currentEmptyArea = 0;
    int currentStartingIndex = -1;
    int longestStartingIndex = -1;
    int initIndex = -1;

    for (int i = 0; i < size; i++) {
        if (table[i].hashAddress == -1) {
            if (currentEmptyArea == 0) {
                currentStartingIndex = i;
            }
            currentEmptyArea++;
        } else {
            if(initIndex == -1){
                initIndex = i; // Index of first non-empty spot
            }
            if (currentEmptyArea > longestEmptyArea) {
                longestEmptyArea = currentEmptyArea;
                longestStartingIndex = currentStartingIndex;
            }
            currentEmptyArea = 0;
        }
    }
    for(int i = 0; i < initIndex; i++){
        currentEmptyArea++; // Count overflow
    }

    if (currentEmptyArea > longestEmptyArea) {
        longestEmptyArea = currentEmptyArea;
        longestStartingIndex = currentStartingIndex;
    }

    if (longestEmptyArea > 0) {
        printf("Longest empty area: %d\n", longestEmptyArea);
        printf("Starting index of longest empty area: %d\n", longestStartingIndex);
    } else {
        printf("No empty areas found in the table.\n");
    }
}

void findLongestCluster(HashEntry* table, int size) {
    int longestCluster = 0;
    int currentCluster = 0;
    int currentStartingIndex = -1;
    int longestStartingIndex = -1;
    int initIndex = -1;

    for (int i = 0; i < size; i++) {
        if (table[i].hashAddress != -1) {
            if (currentCluster == 0) {
                currentStartingIndex = i;
            }
            currentCluster++;
        } else {
            if(initIndex == -1){
                initIndex = i; // Index of first non-empty spot
            }
            if (currentCluster > longestCluster) {
                longestCluster = currentCluster;
                longestStartingIndex = currentStartingIndex;
            }
            currentCluster = 0;
        }
    }
    for(int i = 0; i < initIndex; i++){
        currentCluster++; // Count overflow
    }

    if (currentCluster > longestCluster) {
        longestCluster = currentCluster;
        longestStartingIndex = currentStartingIndex;
    }

    if (longestCluster > 0) {
        printf("Longest Cluster: %d\n", longestCluster);
        printf("Starting index of longest Cluster: %d\n", longestStartingIndex);
    } else {
        printf("No Clusters found in the table.\n");
    }
}

void findMaxDistinctHash(HashEntry* table, int size) {
    int hashcounts[size];

    for(int i = 0; i < size; i++){
        hashcounts[i] = 0;
    }

    for (int i = 0; i < size; i++) {
        if (table[i].hashAddress != -1) {
            hashcounts[table[i].hashAddress]++;
        }
    }

    int largestHash = -1;
    int largestHashCount = -1;

    for(int i = 0; i < size; i++){
        if(hashcounts[i] > largestHashCount){
            largestHash = i;
            largestHashCount = hashcounts[i];
        }
    }

    if (largestHash != -1) {
        printf("Hash value with the greatest number of distinct words (first if multiple): %d\n", largestHash);
        printf("Number of words with that hash value: %d\n", largestHashCount);
    } else {
        printf("No distinct words found in the table.\n");
    }
}

void findFarthestWord(HashEntry* table, int size) {
    int maxDistance = 0;
    int farthestIndex = -1;

    for (int i = 0; i < size; i++) {
        if (table[i].hashAddress != -1) {
            int actualHash = table[i].hashValue;
            int distance = (i - actualHash + size) % size;

            if (distance > maxDistance) {
                maxDistance = distance;
                farthestIndex = i;
            }
        }
    }

    if (farthestIndex != -1) {
        printf("Word farthest from its actual hash value: %s\n", table[farthestIndex].hashedWord);
        printf("Distance from actual hash value: %d\n", maxDistance);
        printf("Index: %d\n", farthestIndex);
    } else {
        printf("No words found in the table.\n");
    }
}

int main() {
    char filename[MAX_FILENAME_LENGTH];
    int tableSize;

    printf("Enter the name of the file: ");
    scanf("%s", filename);

    printf("Enter the size of the table: ");
    scanf("%d", &tableSize);

    FILE* file = fopen(filename, "r");

    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    HashEntry* hashTable;
    initializeTable(&hashTable, tableSize);

    char buffer[256];

    while (fscanf(file, "%s", buffer) == 1) {
        char newBuffer[256];
        removePeriodsAndCommas(buffer, newBuffer);
        int wordLength = strlen(newBuffer);
        int hashValue = hash(newBuffer, wordLength, tableSize);
        insertIntoTable(hashTable, hashValue, newBuffer, hashValue, tableSize);
    }

    fclose(file);

    // Display the contents of the hash table
    displayTable(hashTable, tableSize);
    calculateLoadFactor(hashTable, tableSize);
    findLongestEmptyArea(hashTable, tableSize);
    findLongestCluster(hashTable, tableSize);
    findMaxDistinctHash(hashTable, tableSize);
    findFarthestWord(hashTable, tableSize);

    // Free allocated memory
    for (int i = 0; i < tableSize; i++) {
        if (hashTable[i].hashedWord != NULL) {
            free(hashTable[i].hashedWord);
        }
    }
    free(hashTable);

    return 0;
}
