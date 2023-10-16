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
                # TODO CHANGE
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
            self.get_move()

        self.print_status()

        if self.condition == "win":
            if self.player:
                print("Player X won!")
            else:
                print("Player O won!")
        else:
            print("It's a Draw!")


if __name__ == '__main__':
    game = Game()
    game.play()
