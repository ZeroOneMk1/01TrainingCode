import random
from colorama import Fore, Back
import matplotlib.pyplot as plt

CRAFTING = 7
DC = 15
ROUNDS_PER_MINUTE = 10
ROUNDS_CRIT_HOLDS = ROUNDS_PER_MINUTE
ASSURANCE = True

SIM_LENGTH = 8*ROUNDS_PER_MINUTE
NUMBER_OF_SIMS = 10000

overdrives = []
rd = random.Random()
for i in range(NUMBER_OF_SIMS):
    overdrives.append([])
    status = 0
    for j in range(SIM_LENGTH):

        if status == 0:
            if ASSURANCE:
                temp = 10 + CRAFTING
            else:
                temp = rd.randint(1, 20) + CRAFTING
            
            if temp >= DC + 10:
                status = 2
            elif temp >= DC:
                status = 1
            else:
                status = 0

        elif status == 1:
            temp = rd.randint(1, 20) + CRAFTING
            if temp >= DC + 10:
                status = 2
            else:
                status = 1
        
        if status == 2:
            for k in range(ROUNDS_CRIT_HOLDS):
                overdrives[i].append(2)
            j += ROUNDS_CRIT_HOLDS
            status = 0
        else:
            overdrives[i].append(status)

nones = 0
ones = 0
twos = 0
status = 0
data = []
for i in range(SIM_LENGTH):
    string  = ''
    distribution = 0
    for j in range(NUMBER_OF_SIMS):
        status = overdrives[j][i]
        if status == 0:
            string += f"{Fore.RED + Back.RED} "
            nones += 1
        elif status == 1:
            string += f"{Fore.YELLOW + Back.YELLOW} "
            distribution += 1
            ones += 1
        else:
            string += f"{Fore.GREEN + Back.GREEN} "
            distribution += 2
            twos += 1
    data.append(distribution/NUMBER_OF_SIMS)
    string += f"{Fore.CYAN + Back.RESET} {distribution/NUMBER_OF_SIMS:.2f}"
    string += f"{Fore.RESET + Back.RESET}"
    # print(string)
print(f"{Fore.RESET + Back.RESET}\n\n0: {nones/SIM_LENGTH/NUMBER_OF_SIMS}\n1: {ones/SIM_LENGTH/NUMBER_OF_SIMS}\n2: {twos/SIM_LENGTH/NUMBER_OF_SIMS}")
# plt.plot(data)
# plt.show()