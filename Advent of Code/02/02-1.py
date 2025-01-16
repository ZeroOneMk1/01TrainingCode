import re
with open("02/input.txt", "r") as f:
    strin = f.read()
    lines = strin.split("\n")
    newl = []
    for line in lines:
        if(not (re.search(r"\b(?:1[5-9]|[2-9]\d+)\s*blue\b", line) is not None or re.search(r"(?:1[4-9]|[2-9]\d+)(?=\s*green)", line) is not None or re.search(r"\b(?:1[3-9]|[2-9]\d+)\s*red\b", line) is not None)):
            newl.append(line)
    ids = []
    for line in newl:
        ids.append(re.findall(r"Game ([\d]+)",line))
    sum = 0
    for id in ids:
        sum += int(id[0])
    
    print(sum)