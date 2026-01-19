import re

action = "2x (Bite, Claw), Longsword, Crax (If Grappled & Restrained), 4x (Fire Breath, Tail Swipe, Wing Attack)"

# split the 2x (A, B) into 2 A, 2 B without breaking any words that have x in them
action = re.sub(r'(\d+)x \(([\w\W]+?)\)', lambda m: ', '.join([f"{m.group(1)} {attack.strip()}" for attack in m.group(2).split(',')]), action)

print(action)  # Output: "2 Bite, 2 Claw, Longsword, Crax"

counterbetters = ["A", "B"]
counterbettercount = 2
for browsertwo, i in zip(counterbetters, range(counterbettercount)):
    print(browsertwo, i)