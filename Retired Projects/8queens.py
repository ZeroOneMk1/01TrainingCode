class Board():

    def __init__(self):
        self.squares = []
        self.queens = []

        for i in range(8):
            for j in range(8):
                self.squares.append((i, j))

    def __repr__(self):
        out = ""
        for i in range(8):
            for j in range(8):
                if (i, j) in self.squares:
                    out += "O"
                elif (i, j) in self.queens:
                    out += "X"
                else:
                    out += "#"
            out += "\n"
        return out
    
    def play(self, i, j):
        
        if (i, j) not in self.squares:
            return False
        
        self.place_queen(i, j)
        return True

    def place_queen(self, i, j):
        self.queens.append((i, j))
        self.remove_vert_squares(i)
        self.remove_hor_squares(j)
        self.remove_diag_squares(i, j)
    
    def remove_vert_squares(self, i):
        to_remove = []
        for square in self.squares:
            if square[0] == i:
                to_remove.append(square)
        for square in to_remove:
            self.squares.remove(square)

    def remove_hor_squares(self, j):
        to_remove = []
        for square in self.squares:
            if square[1] == j:
                to_remove.append(square)
        for square in to_remove:
            self.squares.remove(square)

    def remove_diag_squares(self, i, j):
        to_remove = []
        for square in self.squares:
            if square[1] - square[0] == j - i:
                to_remove.append(square)
            elif square[1] + square[0] == i + j:
                to_remove.append(square)
        for square in to_remove:
            self.squares.remove(square)


class Tryer:

    def __init__(self):
        self.moves = []

        for first in range(8):

            for second in range(8):

                if second != first:

                    for third in range(8):

                        if third != second and third != first:

                            for fourth in range(8):

                                if fourth != first and fourth != second and fourth != third:

                                    for fifth in range(8):

                                        if fifth != fourth and fifth != third and fifth != second and fifth != first:

                                            for sixth in range(8):

                                                if sixth != fifth and sixth != fourth and sixth != third and sixth != second and sixth != first:

                                                    for seventh in range(8):

                                                        if seventh != sixth and seventh != fifth and seventh != fourth and seventh != third and seventh != second and seventh != first:

                                                            for eigth in range(8):

                                                                if eigth != seventh and eigth != sixth and eigth != fifth and eigth != fourth and eigth != third and eigth != second and eigth != first:

                                                                    self.moves.append((first, second, third, fourth, fifth, sixth, seventh, eigth))
    
    def try_moves(self):
        winners = []
        for move in self.moves:
            board = Board()
            for i in range(8):
                if not board.play(i, move[i]):
                    break
                if i == 7:
                    winners.append(move)
        return winners
            

if __name__ == '__main__':
    tryer = Tryer()
    winners = tryer.try_moves()

    for winner in winners:
        board = Board()
        for i in range(8):
            if not board.play(i, winner[i]):
                break
            if i == 7:
                print(board)


