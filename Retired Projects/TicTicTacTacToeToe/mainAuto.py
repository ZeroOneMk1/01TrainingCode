from random import randint as rd
from time import time

class Smol():
    def __init__(self):
        self.squares = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]

    def make_move(self, row: int, col: int, player: bool) -> bool:
        """Makes a move. If succesful, returns True, else returns false."""

        if self.squares[row][col] is None:
            self.squares[row][col] = player
            return True
        else:
            return False

    def check_win(self, player: bool) -> bool:
        """Returns whether or not this player just won on this board."""

        for row in range(3):
            if player == self.squares[row][0] == self.squares[row][1] == self.squares[row][2]:
                return True

        for col in range(3):
            if player == self.squares[0][col] == self.squares[1][col] == self.squares[2][col]:
                return True

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] == player:
            return True

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] == player:
            return True

        return False

    def check_draw(self) -> bool:
        for row in range(3):
            if None in self.squares[row]:
                return False
        return True

    def get_row_repr(self, row: int) -> str:
        out = ""
        for col in range(3):
            if self.squares[row][col] is None:
                out += " "
            elif self.squares[row][col]:
                out += "X"
            else:
                out += "O"

        return out


class Game():
    def __init__(self):
        self.boards = [[Smol(), Smol(), Smol()],
                       [Smol(), Smol(), Smol()],
                       [Smol(), Smol(), Smol()]]

        self.start_board()

        self.player = False
        self.condition = "win"

    def next_player(self):
        self.player = not self.player

    def start_row(self):
        try:
            curr_row = int(input("Which Row would you like to start in?"))
        except:
            print("Invalid input")
            self.start_row()

        if 0 <= curr_row <= 2:
            self.row = curr_row
        else:
            print("Invalid input")
            self.start_row()

    def start_col(self):
        try:
            curr_col = int(input("Which Column would you like to start in?"))
        except:
            print("Invalid input")
            self.start_col()

        if 0 <= curr_col <= 2:
            self.col = curr_col
        else:
            print("Invalid input")
            self.start_col()

    def start_board(self):
        self.start_row()
        self.start_col()

    def ask_row(self):
        try:
            curr_row = int(input("Which Row would you like to play?"))
        except:
            print("Invalid input")
            self.ask_row()

        if 0 <= curr_row <= 2:
            self.small_row = curr_row
        else:
            print("Invalid input")
            self.ask_row()

    def ask_col(self):
        try:
            curr_col = int(input("Which Column would you like to play?"))
        except:
            print("Invalid input")
            self.ask_col()

        if 0 <= curr_col <= 2:
            self.small_col = curr_col
        else:
            print("Invalid input")
            self.ask_col()

    def ask_move(self):

        self.ask_row()
        self.ask_col()

    def print_status(self):
        out = "\n#############\n"

        for board_row in range(3):
            for sub_row in range(3):
                out += "#" + self.boards[board_row][0].get_row_repr(sub_row) + "#" + self.boards[board_row][1].get_row_repr(
                    sub_row) + "#" + self.boards[board_row][2].get_row_repr(sub_row) + "#\n"
            out += "#############\n"

        if self.player:
            out += "Player X's turn.\n"
        else:
            out += "Player O's turn.\n"

        out += f"Currently playing on board ({self.row}, {self.col})"

        print(out)

    def get_move(self):
        self.ask_move()
        if not self.boards[self.row][self.col].make_move(self.small_row, self.small_col, self.player):
            print("That space is already full. Please try a different move.")
            self.get_move()

    def check_wins(self, board_row, board_col) -> None or int:
        if self.boards[board_row][board_col].check_win(True):
            return 1
        elif self.boards[board_row][board_col].check_win(False):
            return -1
        elif self.boards[board_row][board_col].check_draw():
            return 0
        return None

    def find_random_open_move(self, board_row, board_col) -> tuple:
        best_moves = []
        for row in range(3):
            for col in range(3):
                if self.boards[board_row][board_col].squares[row][col] is None:
                    best_moves.append((row, col))
        return best_moves[rd(0, len(best_moves) - 1)]
                    
    def best_move(self, board_row: int, board_col: int, player: bool) -> tuple:
        
        best_move = self.find_random_open_move(board_row, board_col)

        best_score = self.minmax(best_move[0], best_move[1], not player, 0)

        print(f"Started with the random move {best_move}")

        equal_moves = [best_move]

        if player:
            for row in range(3):
                for col in range(3):
                    if self.boards[board_row][board_col].squares[row][col] is None:
                        
                        self.boards[board_row][board_col].squares[row][col] = player


                        score = self.check_wins(board_row, board_col)

                        if score is None:
                            score = self.minmax(row, col, not player, 0)

                        self.boards[board_row][board_col].squares[row][col] = None

                        if score == best_score:
                            equal_moves.append((row, col))
                        if score > best_score:
                            best_score = score
                            best_move = (row, col)
                            equal_moves.clear()
                            equal_moves.append(best_move)
                            print(f"Found a better move: {best_move}")
                        if score == 1 or best_score == 1:
                            print(f"FORCED WIN, with the move {best_move}")
                            return best_move
        else:
            for row in range(3):
                for col in range(3):
                    if self.boards[board_row][board_col].squares[row][col] is None:
                        
                        self.boards[board_row][board_col].squares[row][col] = player


                        score = self.check_wins(board_row, board_col)

                        if score is None:
                            score = self.minmax(row, col, not player, 0)
                        
                        self.boards[board_row][board_col].squares[row][col] = None

                        if score == best_score:
                            equal_moves.append((row, col))
                        if score < best_score:
                            best_score = score
                            best_move = (row, col)
                            equal_moves.clear()
                            equal_moves.append(best_move)
                            print(f"Found a better move: {best_move}")
                        if score == -1 or best_score == -1:
                            print(f"FORCED WIN, with the move {best_move}")
                            return best_move
        
        chosen_move = equal_moves[rd(0, len(equal_moves) - 1)]

        # TODO The Bot does not take winning moves if the enemy can "win" in the next move
        # TODO Update: not always ???

        if player:
            if best_score == -1:
                print(f"FORCED LOSS, with the move {chosen_move}")
            else:
                print(f"failed maximizing, with the move {chosen_move}")
        else:
            if best_score == 1:
                print(f"FORCED LOSS, with the move {chosen_move}")
            else:
                print(f"failed minimizing, with the move {chosen_move}")
        return chosen_move

    def true_search(self, board_row, board_col, player, depth):
        bestScore = -2 ## worst possible outcome for X
        for row in range(3):
            for col in range(3):
                if self.boards[board_row][board_col].squares[row][col] is None:

                    self.boards[board_row][board_col].squares[row][col] = player

                    curr_status = self.check_wins(board_row, board_col)
                    if curr_status is not None:
                        score = curr_status
                        if score > bestScore:
                            bestScore = score
                        if bestScore == 1:
                            self.boards[board_row][board_col].squares[row][col] = None
                            return bestScore
                    
                    score = self.minmax(row, col, not player, depth + 1)
                    self.boards[board_row][board_col].squares[row][col] = None

                    if score > bestScore:
                        bestScore = score
                    if bestScore == 1:
                        return bestScore
        return bestScore

    def false_search(self, board_row, board_col, player, depth):
        bestScore = 2 # worst possible outcome for O
        for row in range(3):
            for col in range(3):
                if self.boards[board_row][board_col].squares[row][col] is None:

                    self.boards[board_row][board_col].squares[row][col] = player

                    curr_status = self.check_wins(board_row, board_col)
                    if curr_status is not None:
                        score = curr_status
                        if score < bestScore:
                            bestScore = score
                        if bestScore == -1:
                            self.boards[board_row][board_col].squares[row][col] = None
                            return bestScore

                    score = self.minmax(row, col, not player, depth + 1)
                    self.boards[board_row][board_col].squares[row][col] = None

                    if score < bestScore:
                        bestScore = score
                    if bestScore == -1:
                        return bestScore
        return bestScore

    def minmax(self, board_row, board_col, player, depth) -> int:

        result = self.check_wins(board_row, board_col)
        if result is not None:
            return result

        if depth == 8:
            return 0

        if player:
            return self.true_search(board_row, board_col, player, depth)
        else:
            return self.false_search(board_row, board_col, player, depth)
                        
    def get_if_minmaxing(self) -> bool:
        try:
            return bool(int(input("Do you want this move to be automatic?")))
        except:
            return self.get_if_minmaxing()

    def play(self):
        while not self.boards[self.row][self.col].check_win(self.player):
            self.next_player()
            try:
                self.row = self.small_row
                self.col = self.small_col
            except:
                print("A")

            if self.boards[self.row][self.col].check_draw():
                self.condition = "draw"
                break

            self.print_status()

            # not self.get_if_minmaxing() vvvvvvvv
            
            # if self.player:
            #     self.get_move()
            #     # rand_move = self.find_random_open_move(self.row, self.col)
            #     # print(f"The random agent chose the move {rand_move}")
            #     # self.small_row = rand_move[0]
            #     # self.small_col = rand_move[1]
            #     # self.boards[self.row][self.col].make_move(self.small_row, self.small_col, self.player)
            # else:
            bestmove = self.best_move(self.row, self.col, self.player)
            self.small_row = bestmove[0]
            self.small_col = bestmove[1]
            self.boards[self.row][self.col].make_move(self.small_row, self.small_col, self.player)

        self.print_status()

        if self.condition == "win":
            if self.player:
                print("Player 1 (X) won!")
            else:
                print("Player 2 (O) won!")
        else:
            print("It's a Draw!")


if __name__ == '__main__':
    game = Game()
    start = time()
    game.play()
    print(f"The game took {time() - start} seconds")
