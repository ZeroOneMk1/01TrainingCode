class Tower:
    def __init__(self, num_stacked: int):
        self.stacks = [[], [], []]
        self.num_stacked = num_stacked
        self.instructions = ''

        for i in reversed(range(num_stacked)):
            self.stacks[0].append(i)

    def __repr__(self) -> str:
        out = ""
        for i in reversed(range(self.num_stacked)):
            currout = ""

            try:
                currout += str(self.stacks[0][i])
            except:
                currout += " "
            currout += "  "
            try:
                currout += str(self.stacks[1][i])
            except:
                currout += " "
            currout += "  "
            try:
                currout += str(self.stacks[2][i])
            except:
                currout += " "

            currout += "\n"
            out += currout
        return out

    def move_the_above(self, current: int, to_move: int, other: int, working: int) -> None:
        if self.stacks[current][-1] != working:
            self.move_the_above(current, other, to_move, working - 1)

            self.stacks[to_move].append(self.stacks[current].pop())
            self.instructions += self.__repr__()

            self.move_the_above(other, to_move, current, working - 1)
        else:
            self.stacks[to_move].append(self.stacks[current].pop())
            self.instructions += self.__repr__()
        

if __name__ == '__main__':
    tower = Tower(8)

    tower.move_the_above(0, 2, 1, tower.num_stacked - 1)
    with open("instructions.txt", 'w') as f:
            f.write(tower.instructions)
