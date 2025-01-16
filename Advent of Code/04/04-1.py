import re

with open("04/input.txt", "r") as f:
    strin = f.read()

    a = re.findall(r":([^|]+)\|([^\n]+)", strin)

    winners = [row[0] for row in a]
    ours = [row[1] for row in a]

    winnern = [re.findall(r"(\d+)", row) for row in winners]
    ourn = [re.findall(r"(\d+)", row) for row in ours]

    winnernint = []
    ournint = []

    for row in winnern:
        winnernint.append([int(i) for i in row])

    for row in ourn:
        ournint.append([int(i) for i in row])

    sum = 0

    for i in range(len(winnernint)):
        set1 = set(winnernint[i])
        set2 = set(ournint[i])

        overlap = set1.intersection(set2)
        count_overlap = len(overlap)

        if count_overlap != 0:
            sum += 2**(count_overlap - 1)


    print(sum)


    