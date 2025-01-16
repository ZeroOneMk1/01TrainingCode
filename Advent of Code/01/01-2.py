import re

with open("Advent of Code/01/input.txt", 'r') as f:
    strin = f.read()

    strin = strin.replace("nine", "nine9nine")
    strin = strin.replace("eight", "eight8eight")
    strin = strin.replace("seven", "seven7seven")
    strin = strin.replace("six", "six6six")
    strin = strin.replace("five", "five5five")
    strin = strin.replace("four", "four4four")
    strin = strin.replace("three", "three3three")
    strin = strin.replace("two", "two2two")
    strin = strin.replace("one", "one1one")
    # strin.replace("zero", "zero0zero")

    strin = re.sub(r"[^\d\n]", "", strin)

    firsts = re.findall(r"\n(\d)", strin)
    lasts = re.findall(r"(\d)\n", strin)

    nums = []
    print(len(firsts), len(lasts))
    if(len(firsts) == len(lasts)):
        for i in range(len(firsts)):
            nums.append(firsts[i] + lasts[i])

    sum = 0
    for num in nums:
        sum += int(num)

    print(sum)