import re
with open("02/input.txt", "r") as f:
    strin = f.read()
    lines = strin.split("\n")
    pows = []
    for line in lines:
        matches = re.findall(r'\b(\d+)(?=\s*red\b)', line)
        largest_red = max(map(int, matches))
        matches = re.findall(r'\b(\d+)(?=\s*green\b)', line)
        largest_green = max(map(int, matches))
        matches = re.findall(r'\b(\d+)(?=\s*blue\b)', line)
        largest_blue = max(map(int, matches))
        pows.append(largest_red*largest_blue*largest_green)
    sum = 0
    for pow in pows:
        sum += int(pow)
    
    print(sum)