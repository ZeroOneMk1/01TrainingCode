import regex as re
from random import randint as ri
from math import log, floor
import gmpy

def get_nimsum(board):
    nimsum = 0

    for i in range(len(board)):
        nimsum = nimsum ^ board[i]
    
    print(f"NIMSUM: {nimsum}")
    return nimsum

def get_lsb_ind(board):
    lsbs_us = []
    for i in range(len(board)):
        lsbs_us.append(gmpy.scan1(board[i]) + 1)
    
    lsbs_s = [lsbs_us[i] for i in range(len(lsbs_us))]
    lsbs_s.sort()

    return lsbs_us, lsbs_s

def find_best_move(board):
    nimsum = get_nimsum(board)

    if nimsum != 0:

        msbn = floor(log(nimsum)/log(2) + 1)

        msbs = [floor(log(num + 0.9999999)/log(2)) + 1 for num in board]

        for i in range(len(board)):
            if msbn <= msbs[i]:
                if board[i] & 2**(msbn-1):
                    break
        
        bxn = board[i]^nimsum
        
        best_move = (i, (board[i]-bxn - 1)%board[i] + 1)
    else:
        lsbs_us, lsbs_s = get_lsb_ind(board)
        i = 0
        while(i < len(lsbs_s)):
            if lsbs_s[i] > 0:
                break
            i += 1
        
        to_remove_from = find_first_instance(lsbs_us, lsbs_s[i])
        best_move = (to_remove_from, 1)

    return best_move

def find_first_instance(lsbs, lsb):
    for i in range(len(lsbs)):
        if lsb == lsbs[i]:
            return i

    return -1

def game_over(board):
    if(sum(board) == 0):
        return True
    else:
        return False


def make_move(board, move):
    temp_board = [board[i] for i in range(len(board))]
    temp_board[move[0]] -= move[1]
    return temp_board


if __name__ == "__main__":
    board = [ri(0, 32) for i in range(ri(3, 8))]
    # board = [3, 7, 5]
    print(board)

    if(get_nimsum(board) == 0):
        print("PREDICT P2 WIN")
    else:
        print("PREDICT P1 WIN")

    player = True

    playing = False

    if not playing:
        while(sum(board) != 0):
            best_move = find_best_move(board)
            print("Best Move:", best_move)
            board = make_move(board, best_move)
            print(board)
            player = not player
    else:
        while(sum(board) != 0):
            if not player:
                best_move = find_best_move(board)
                print("Best Move:", best_move)
                board = make_move(board, best_move)
                print(board)
            else:
                movestr = input("What move do you want to play?")
                move = re.findall(r"[\d]+", movestr)
                for i in range(len(move)):
                    move[i] = int(move[i])
                print(f"Your Move: {move}")
                board = make_move(board, move)
                print(board)

            player = not player
    
    if player:
        print("Player 2 wins!")
    else:
        print("Player 1 wins!")
