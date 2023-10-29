import regex as r
        
def minimax(board, depth, maximizing_player):
    if game_over(board):
        return (-1)**(not maximizing_player)
        
    if depth == 0:
        return 0

    if maximizing_player:
        best_value = -float("inf")
        for move in legal_moves(board):
            new_board = make_move(board, move)
            value = minimax(new_board, depth - 1, False)
            best_value = max(best_value, value)
        return best_value
    else:
        best_value = float("inf")
        for move in legal_moves(board):
            new_board = make_move(board, move)
            value = minimax(new_board, depth - 1, True)
            best_value = min(best_value, value)
        return best_value

def find_best_move(board, depth, player):
    best_move = None
    best_value = -float("inf")
    for move in legal_moves(board):
        new_board = make_move(board, move)
        value = minimax(new_board, depth - 1, False)
        if value > best_value:
            best_value = value
            best_move = move
        elif(value == best_value):
            if value == 1:
                if(best_move[1] < move[1]):
                    best_value = value
                    best_move = move
            elif value == -1:
                if(best_move[1] > move[1]):
                    best_value = value
                    best_move = move
                    

    return best_move

def game_over(board):
    if(sum(board) == 0):
        return True
    else:
        return False

def legal_moves(board):
    list = []
    for i in range(board[0]):
        list.append((0, i + 1))
    for i in range(board[1]):
        list.append((1, i + 1))
    for i in range(board[2]):
        list.append((2, i + 1))
    return list

def make_move(board, move):
    temp_board = [board[i] for i in range(3)]
    temp_board[move[0]] -= move[1]
    return temp_board


if __name__ == "__main__":
    board = [3, 7, 5]

    player = True

    while(sum(board) != 0):
        if not player:
            best_move = find_best_move(board, 8, player)
            print("Best Move:", best_move)
            board = make_move(board, best_move)
            print(board)
        else:
            best_move = find_best_move(board, 8, player)
            print("Best Move:", best_move)
            board = make_move(board, best_move)
            print(board)
            # movestr = input("What move do you want to play?")
            # move = r.findall(r"\d", movestr)
            # for i in range(len(move)):
            #     move[i] = int(move[i])
            # print(f"Your Move: {move}")
            # board = make_move(board, move)
            # print(board)

        player = not player
    
    if player:
        print("Player 2 wins!")
    else:
        print("Player 1 wins!")
