import re

with open("01/input.txt", 'r') as f:
    strin = f.read()
    strin = re.sub(r"[^\d\n]", "", strin)

    firsts = re.findall(r"\n(\d)", strin)
    lasts = re.findall(r"(\d)\n", strin)

    nums = []
    if(len(firsts) == len(lasts)):
        for i in range(len(firsts)):
            nums.append(firsts[i] + lasts[i])

    sum = 0
    for num in nums:
        sum += int(num)

    print(sum)