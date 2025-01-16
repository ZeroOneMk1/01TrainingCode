def find_adjacent_numbers(matrix, row, col):
    nums = []
    try:
        if(matrix[row-1][col].isdigit()):
            num = matrix[row-1][col]
            propcol = col-1
            try:
                while(matrix[row-1][propcol].isdigit()):
                    num = matrix[row-1][propcol]+ num
                    propcol -= 1
            except:
                pass
            propcol = col+1
            try:
                while(matrix[row-1][propcol].isdigit()):
                    num += matrix[row-1][propcol]
                    propcol += 1
            except:
                pass
            nums.append(int(num))
    except:
            pass
    
    if(len(nums) == 0):
        try:
            if(matrix[row-1][col-1].isdigit()):
                num = matrix[row-1][col-1]
                propcol = col-2
                try:
                    while(matrix[row-1][propcol].isdigit()):
                        num = matrix[row-1][propcol] + num
                        propcol -= 1
                except:
                    pass
                nums.append(int(num))
        except:
            pass
        try:
            if(matrix[row-1][col+1].isdigit()):
                num = matrix[row-1][col+1]
                propcol = col+2
                try:
                    while(matrix[row-1][propcol].isdigit()):
                        num += matrix[row-1][propcol]
                        propcol += 1
                except:
                    pass
                nums.append(int(num))
        except:
            pass

    lens = len(nums)

    try:
        if(matrix[row+1][col].isdigit()):
            num = matrix[row+1][col]
            propcol = col-1
            try:
                while(matrix[row+1][propcol].isdigit()):
                    num = matrix[row+1][propcol] + num
                    propcol -= 1
            except:
                pass
            propcol = col+1
            try:
                while(matrix[row+1][propcol].isdigit()):
                    num += matrix[row+1][propcol]
                    propcol += 1
            except:
                pass
            nums.append(int(num))
    except:
            pass


    if(len(nums)==lens):
        try:
            if(matrix[row+1][col-1].isdigit()):
                num = matrix[row+1][col-1]
                propcol = col-2
                try:
                    while(matrix[row+1][propcol].isdigit()):
                        num = matrix[row+1][propcol] + num
                        propcol -= 1
                except:
                    pass
                nums.append(int(num))

        except:
            pass
        if(matrix[row+1][col+1].isdigit()):
            num = matrix[row+1][col+1]
            propcol = col+2
            try:
                while(matrix[row+1][propcol].isdigit()):
                    num += matrix[row+1][propcol]
                    propcol += 1
            except:
                pass
            nums.append(int(num))
    
    try:
        if(matrix[row][col-1].isdigit()):
            num = matrix[row][col-1]
            propcol = col-2
            try:
                while(matrix[row][propcol].isdigit()):
                    num = matrix[row][propcol] + num
                    propcol -= 1
            except:
                pass
            nums.append(int(num))
    except:
        pass

    try:
        if(matrix[row][col+1].isdigit()):
            num = matrix[row][col+1]
            propcol = col+2
            try:
                while(matrix[row][propcol].isdigit()):
                    num += matrix[row][propcol]
                    propcol += 1
            except:
                pass
            nums.append(int(num))
    except:
        pass


    if(len(nums) ==2):
        return nums
    else:
        return None

def process_matrix(matrix):
    total_sum = 0

    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == '*':
                adjacent_numbers = find_adjacent_numbers(matrix, row, col)
                if adjacent_numbers is not None:
                    total_sum += adjacent_numbers[0]*adjacent_numbers[1]

    return total_sum


with open("03/input.txt", "r") as f:
    strin = f.read()

    matrix = strin.split('\n')

    result = process_matrix(matrix)
    print(result)
