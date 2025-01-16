import re
import math

def is_symbol(char):
    return not (char.isdigit() or char == '.')

def find_adjacent_symbols(engine_schematic, row, start, end):    

    for i in range(row - 1, row + 2):
        for j in range(start - 1, end + 1):
            if 0 <= i < len(engine_schematic) and 0 <= j < len(engine_schematic[i]):
                if is_symbol(engine_schematic[i][j]):
                    return True

    return False

def sum_part_numbers(engine_schematic):
    total_sum = 0

    for row in range(len(engine_schematic)):
        num = 0
        wasdigit = 0
        for col in range(len(engine_schematic[row])):
            char = engine_schematic[row][col]

            if char.isdigit():
                if not wasdigit:
                    wasdigit = 1
                    num = int(char)
                    initcol = col
                else:
                    num *= 10
                    num += int(char)
            elif wasdigit:
                wasdigit = 0
                if (find_adjacent_symbols(engine_schematic, row, initcol, col)):
                    total_sum += num
                num = 0

    return total_sum

# Example engine schematic



with open("03/input.txt", "r") as f:
    strin = f.read()

    engine_schematic = strin.split('\n')

    result = sum_part_numbers(engine_schematic)
    print("Sum of all part numbers in the engine schematic:", result)
