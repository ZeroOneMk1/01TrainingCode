import re

def proc(card, winnernint, ournint, instances):
    instances[card] += 1
    set1 = set(winnernint[card])
    set2 = set(ournint[card])

    overlap = set1.intersection(set2)
    count_overlap = len(overlap)

    sum = 1

    if(count_overlap != 0):
        for i in range(1, count_overlap + 1):
            if(card + i < len(winnernint)):
                sum += proc(card + i, winnernint, ournint, instances)
        
    return sum

with open("04/input.txt", "r") as f:
    strin = f.read()

    a = re.findall(r":([^|]+)\|([^\n]+)", strin)

    winners = [row[0] for row in a]
    ours = [row[1] for row in a]

    winnern = [re.findall(r"(\d+)", row) for row in winners]
    ourn = [re.findall(r"(\d+)", row) for row in ours]

    winnernint = []
    ournint = []
    instances = [0 for i in range(len(ourn))]

    for row in winnern:
        winnernint.append([int(i) for i in row])

    for row in ourn:
        ournint.append([int(i) for i in row])

    sum = 0

    for i in range(len(ournint)):
        sum += proc(i, winnernint, ournint, instances)        

    print(instances)
    print(sum)


    