
wii_sports_durs = [.25, .25, .75, .25, .5, .5, 3]
wii_new = []

megalovania_durs = [0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
eg_new = []

tie = 0
for i in range(len(wii_sports_durs)):
    wii_new.append(tie)
    tie += 100 * wii_sports_durs[i]
wii_new.append(tie)
print(wii_new)

tie = 0
for i in range(len(megalovania_durs)):
    eg_new.append(tie)
    tie += 100 * megalovania_durs[i]
eg_new.append(tie)
print(eg_new)