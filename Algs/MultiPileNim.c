#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>

#define LARGEST_BIT 6
#define AI 0
#define OPTI 1
#define RANDOMIZED 2
#define GUI 3
#define PLAYCOUNT 4

void ask_for_settings(int*);
unsigned int get_nimsum(unsigned int*, unsigned int);
int compare(const void *, const void *);
void get_lsbs(unsigned int*, unsigned int, unsigned int*, unsigned int*);
unsigned int get_lsb(unsigned int);
void find_best_move(unsigned int*, unsigned int, unsigned int*, unsigned int);
unsigned int get_msb(unsigned int);
unsigned int find_first_instance(unsigned int*, unsigned int, unsigned int);
unsigned int game_over(unsigned int*, unsigned int);
void make_move(unsigned int*, unsigned int*);
void print_board(unsigned int*, unsigned int, int);
unsigned int sum_board(unsigned int*, unsigned int);

int main(){
    int settings[5];
    ask_for_settings(settings);
    srand(time(NULL));

    unsigned int boardlength = 3;
    unsigned int board[] = {3, 7, 5};

    int games_won = 0;

    for(int game = 0; game < settings[PLAYCOUNT]; game++){

        if(settings[RANDOMIZED]){
            boardlength = rand()%7 + 3; // Max 9, min 3
            unsigned int board[boardlength];
            for(unsigned int i = 0; i < boardlength; i++){
                board[i] = rand() % (1 << LARGEST_BIT);
            }
        }
        
        print_board(board, boardlength, settings[GUI]);

        int player = 1;

        if(!settings[AI]){
            player = 0;
            printf("Do you want to play first? 0 - No, 1 - Yes\n");
            scanf("%d", &player);
        }else{
            if(get_nimsum(board, boardlength) == 0){
                printf("PREDICT P2 WIN\n");
            }else{
                printf("PREDICT P1 WIN\n");
            }
        }
        if(settings[AI]){
            while(sum_board(board, boardlength) != 0){
                unsigned int best_move[2];
                find_best_move(board, boardlength, best_move, settings[OPTI]);
                printf("Best Move: [%d, %d]\n", best_move[0], best_move[1]);
                make_move(board, best_move);
                print_board(board, boardlength, settings[GUI]);
                player = !player;
            }
        }else{
            while(sum_board(board, boardlength) != 0){
                if(player){
                    unsigned int best_move[2];
                    printf("What heap would you like to remove from?\n");
                    scanf("%d", &best_move[0]);

                    printf("How many pieces do you wish to remove?\n");
                    scanf("%d", &best_move[1]);
                    make_move(board, best_move);
                    print_board(board, boardlength, settings[GUI]);
                    player = !player;
                }else{
                    unsigned int best_move[2];
                    find_best_move(board, boardlength, best_move, settings[OPTI]);
                    printf("Best Move: [%d, %d]\n", best_move[0], best_move[1]);
                    make_move(board, best_move);
                    print_board(board, boardlength, settings[GUI]);
                    player = !player;
                }
            }
        }
        
        if(player){
            printf("Player 2 wins!\n");
        }else{
            printf("Player 1 wins!\n");
            games_won++;
        }
    }
    printf("Player 1 won %d Games.\nPlayer 2 won %d Games.", games_won, settings[PLAYCOUNT] - games_won);
}
void ask_for_settings(int* settings){
    int ai;
    printf("Should the AI play itself, or do you wish to play? 0 - You, 1 - AI\n");
    scanf("%d", &ai);

    int opti;
    printf("Should the AI lose optimally (Stall if it can't win)? 0 - No, 1 - Yes\n");
    scanf("%d", &opti);

    int rand;
    printf("Should the board be randomized? 0 - No, 1 - Yes\n");
    scanf("%d", &rand);

    int gui;
    printf("Do you want the board to be visualized (Warning, can be illegible if board is randomized)? 0 - Printed, 1 - Visualized\n");
    scanf("%d", &gui);

    int playcount;
    printf("How many games do you wish to play?\n");
    scanf("%d", &playcount);

    settings[0] = ai;
    settings[1] = opti;
    settings[2] = rand;
    settings[3] = gui;
    settings[4] = playcount;
}

unsigned int get_nimsum(unsigned int* board, unsigned int boardlength){
    unsigned int nimsum = 0;

    for(unsigned int i = 0; i < boardlength; i++){
        nimsum = nimsum ^ board[i];
    }

    return nimsum;
}
int compare(const void *a, const void *b) {
    return (*(unsigned int*)a - *(unsigned int*)b);
}
void get_lsbs(unsigned int* board, unsigned int boardlength, unsigned int* lsbs_unsorted, unsigned int* lsbs_sorted){
    for(unsigned int i = 0; i < boardlength; i++){
        lsbs_unsorted[i] = get_lsb(board[i]);
    }
    for(unsigned int i = 0; i < boardlength; i++){
        lsbs_sorted[i] = lsbs_unsorted[i];
    }
    qsort(lsbs_sorted, boardlength, sizeof(unsigned int), compare);
}
unsigned int get_lsb(unsigned int number){
    if(number == 0){
        return 0;
    }
    unsigned int i = 0;
    while(!(number & (0b1 << i))){
        i++;
    }
    return i + 1;
}
void find_best_move(unsigned int* board, unsigned int boardlength, unsigned int* bestmove, unsigned int optimizing){
    unsigned int nimsum = get_nimsum(board, boardlength);

    if(nimsum != 0){
        unsigned int most_significant_bit_nimsum = get_msb(nimsum);

        unsigned int most_significant_bits_board[boardlength];
        for(unsigned int i = 0; i < boardlength; i++){
            most_significant_bits_board[i] = get_msb(board[i]);
        }
        unsigned int i;
        for(i = 0; i < boardlength; i++){
            if(most_significant_bit_nimsum <= most_significant_bits_board[i]){
                if(board[i] & (1 << (most_significant_bit_nimsum-1))){
                    break;
                }
            }
        }

        unsigned int bxn = board[i]^nimsum;

        bestmove[0] = i;
        bestmove[1] = (unsigned int)(((int)board[i]- (int)bxn - 1)%(int)board[i] + 1);
    }else{
        if(optimizing){
            unsigned int lsbs_unsorted[boardlength];
            unsigned int lsbs_sorted[boardlength];
            get_lsbs(board, boardlength, lsbs_unsorted, lsbs_sorted);
            unsigned int i = 0;
            while(i < boardlength){
                if(lsbs_sorted[i] > 0){
                    break;
                }
                i++;
            }
            unsigned int to_remove_from = find_first_instance(lsbs_unsorted, boardlength, lsbs_sorted[i]);
            bestmove[0] = to_remove_from;
            bestmove[1] = 1;
        }else{
            bestmove[0] = 0;
            while(board[bestmove[0]] == 0){
                bestmove[0] = rand()%boardlength;
            }
            bestmove[1] = rand()%board[bestmove[0]] + 1;
        }
    }
}
unsigned int get_msb(unsigned int number){
    if(number == 0){
        return 0;
    }
    unsigned int i = LARGEST_BIT;
    while (!(number & (1 << i))){
        i--;
    }
    return i + 1;
}
unsigned int find_first_instance(unsigned int* lsbs, unsigned int lsbslen, unsigned int lsb){
    for(unsigned int i = 0; i < lsbslen; i++){
        if(lsb == lsbs[i]){
            return i;
        }
    }
    return 0;
}
unsigned int game_over(unsigned int* board, unsigned int boardlength){
    if(sum_board(board, boardlength) == 0){
        return 1;
    }
    return 0;
}
void make_move(unsigned int* board, unsigned int* move){
    board[move[0]] -= move[1];
}
void print_board(unsigned int* board, unsigned int boardlength, int visualize){
    if(visualize){
        unsigned int largest = 0;
        for(unsigned int i = 0; i < boardlength; i++){
            if(board[i] > largest){
                largest = board[i];
            }
        }
        for(unsigned int i = largest; i > 0; i--){
            for(unsigned int j = 0; j < boardlength; j++){
                if(board[j] >= i){
                    printf("0 ");
                }else{
                    printf("  ");
                }
            }
            printf("\n");
        }
        printf("\n");
        for(unsigned int j = 0; j < boardlength; j++){
            printf("%d ", j);
        }
    }else{
        printf("[");
        if (boardlength > 0) {
            printf("%u", board[0]);
            for (size_t i = 1; i < boardlength; i++) {
                printf(", %u", board[i]);
            }
        }
        printf("]");
    }printf("\n");
}
unsigned int sum_board(unsigned int* board, unsigned int boardlength){
    unsigned int sum = 0;
    for(unsigned int i = 0; i < boardlength; i++){
        sum += board[i];
    }
    return sum;
}