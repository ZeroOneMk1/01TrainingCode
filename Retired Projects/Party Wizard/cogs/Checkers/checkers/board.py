from .consts import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.create_board()


    def move(self, startrow, startcol, endrow, endcol, turn):

        if turn == '1' and self.board[startrow][startcol][0] == WHITE:
            moves = self.get_valid_moves(self.board[startrow][startcol])
            
            endmove = (endrow, endcol)

            if endmove not in moves:
                return "That's not a valid move, sorry!"
            else:
                self.board[startrow][startcol], self.board[endrow][endcol] = 0, self.board[startrow][startcol]

                self.board[endrow][endcol][1] = endrow
                self.board[endrow][endcol][2] = endcol

                for piece in moves[(endrow, endcol)]:
                    self.board[piece[1]][piece[2]] = 0

                if self.winner() != 'no':
                    if self.winner() == WHITE:
                        return 'Red wins!!!'
                    else:
                        return 'Purple wins!!!'
                else:
                    return 'No winner yet.'

                if endrow == ROWS - 1 or endrow == 0:
                    self.board[endrow][endcol][3] = True

                    if self.board[endrow][endcol][0] == WHITE:
                        self.board[endrow][endcol][3] = True
                    else:
                        self.board[endrow][endcol][3] = True

        elif turn == '2' and self.board[startrow][startcol][0] == RED:

            moves = self.get_valid_moves(self.board[startrow][startcol])
            endmove = (endrow, endcol)

            if endmove not in moves:
                return "That's not a valid move, sorry!"
            else:
                self.board[startrow][startcol], self.board[endrow][endcol] = 0, self.board[startrow][startcol]

                self.board[endrow][endcol][1] = endrow
                self.board[endrow][endcol][2] = endcol

                for piece in moves[(endrow, endcol)]:
                    self.board[piece[1]][piece[2]] = 0

                if self.winner() != 'no':
                    if self.winner() == WHITE:
                        return 'Red wins!!!'
                    else:
                        return 'Purple wins!!!'
                else:
                    return 'No winner yet.'

                if endrow == ROWS - 1 or endrow == 0:
                    self.board[endrow][endcol][3] = True

                    if self.board[endrow][endcol][0] == WHITE:
                        self.board[endrow][endcol][3] = True
                    else:
                        self.board[endrow][endcol][3] = True
        else:
            return "This isn't your piece!"

        

    def get_piece(self, row, col):
        return self.board[row][col]

    def overwrite(self, boardarr):
        self.board = boardarr["Data"]["Board"]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE).__repr__())
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED).__repr__())
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self):

        numberemotes = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:']

        drawstring = ':zero::one::two::three::four::five::six::seven::eight:\n'
        for row in range(ROWS):
            drawstring += numberemotes[row]
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    if piece[0] == WHITE:
                        if piece[3] == False:
                            drawstring += ':rage:'
                        else:
                            drawstring += ':face_with_symbols_over_mouth:'
                    else:
                        if piece[3] == False:
                            drawstring += ':imp:'
                        else:
                            drawstring += ':smiling_imp:'
                elif col % 2 == 0 and row % 2 == 1:
                    drawstring += ':yellow_square:'
                elif col % 2 == 1 and row % 2 == 0:
                    drawstring += ':yellow_square:'
                else:
                    drawstring += ':brown_square:'
            drawstring += '\n'

        return drawstring

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece[1]][piece[2]] = 0
    
    def winner(self):
        red_left = 0
        white_left = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    if self.board[i][j][0] == RED:
                        red_left += 1
                    else:
                        white_left += 1
        if red_left <= 0:
            return WHITE
        elif white_left <= 0:
            return RED
        else:
            return 'no'
        
        return None 
    
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece[2] - 1
        right = piece[2] + 1
        row = piece[1]
        king = piece[3]
        color = piece[0]

        if color == RED or king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, color, right))
        if color == WHITE or king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, color, right))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current[0] == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current[0] == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    
    def __repr__(self):
        return self.board