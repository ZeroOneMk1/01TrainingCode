import random as rd
import cProfile
import pstats
from Data.road import  Road
from Data.consts import MUTATION_RATE, POPULATION_SIZE, NUM_ALGS, MUTATION_SEVERITY, MUTATION_REPETIVITY
import time

class Finder:

    def __init__(self) -> None:
        self.roads = []
        self.new_roads = []

        # with open("GA for IBCSY2/winners.txt", 'r') as f:
        #     pregenerated = f.readlines()

        #     f.close()
        
        # for road in pregenerated:
        #     self.roads.append(Road(road[:-1], "PREGEN"))


        for i in range(POPULATION_SIZE - len(self.roads)):
            self.roads.append(self.random_road())

    def random_road(self) -> Road:

        cities = ""

        for i in range(25):
            cities += chr(ord('B') + i)
        
        trip = ''.join(rd.sample(cities,len(cities)))

        return Road(trip, "RANDOM")

    def rank(self) -> None:
        
        self.roads.sort(key=lambda x: x.length)

    def generate_children(self, mut_rate: int) -> None:

        for i in range(int((POPULATION_SIZE - mut_rate) / NUM_ALGS / 2)):

            self.breed(self.roads[2*i], self.roads[2*i + 1])

        for i in range(mut_rate):

            self.new_roads.append(self.random_road())

        self.roads = self.new_roads
        self.new_roads = []
    
    def breed(self, r1: Road, r2: Road) -> None:
        self.new_roads.append(Road(r1.trip, r1.type))
        self.new_roads.append(Road(r2.trip, r1.type))
        self.new_roads.append(self.pmx(r1.trip, r2.trip))
        self.new_roads.append(self.pmx(r2.trip, r1.trip))
        self.new_roads.append(self.cx(r1.trip, r2.trip))
        self.new_roads.append(self.cx(r2.trip, r1.trip))
        self.new_roads.append(self.mutate(r1.trip))
        self.new_roads.append(self.mutate(r2.trip))

    def mutate(self, r1: str) -> Road:

        for _ in range(MUTATION_REPETIVITY):

            i_one = rd.randint(0, len(r1) - 1)

            mutation_severity = rd.randint(0, MUTATION_SEVERITY)

            if i_one + mutation_severity >= len(r1):

                i_two = i_one - mutation_severity
            
            else:

                i_two = i_one + mutation_severity
            
            new_trip = ""

            for i in range(len(r1)):

                if i != i_one and i != i_two:
                    new_trip += r1[i]
                elif i == i_one:
                    new_trip += r1[i_two]
                elif i == i_two:
                    new_trip += r1[i_one]
        
        return(Road(new_trip, "MUTATED"))

    def cx(self, r1: str, r2: str) -> Road:

        cycles = []

        cycles = self.find_cycles(r1, r2, cycles)

        childs_arr = []

        for i in range(len(r1)):
            childs_arr.append(0)

        i = -1

        for cycle in cycles:

            i += 1

            if i % 2 == 0:

                for town in cycle:

                    childs_arr[r1.index(town)] = town

            else:

                for town in cycle:

                    childs_arr[r2.index(town)] = town
        
        child_str = ''.join(childs_arr)

        return Road(child_str, "CX")

    def find_cycles(self, r1: str, r2: str, cycles: list) -> list:

        i = self.find_index_not_in_cycles(r1, cycles)

        if i != -1:

            cycles.append(self.find_cycle(r1, r2, i))

            cycles = self.find_cycles(r1, r2, cycles)

            return cycles

        else:

            return cycles

    def find_index_not_in_cycles(self, r1: str, cycles: list) -> int:

        cycles_strf = ""

        for cycle in cycles:
            cycles_strf += ''.join(cycle)

        for letter in r1:

                if letter not in cycles_strf:

                    return r1.index(letter)       

        return -1                      

    def find_cycle(self, r1: str, r2: str, i: int) -> list:

        curr_cycle = []

        while r1[i] not in curr_cycle:

            curr_cycle.append(r1[i])

            i = r2.index(r1[i])

        return curr_cycle

    def pmx(self, r1: str, r2: str) -> Road:

        indices = [rd.randint(0, int(len(r1)/2)), rd.randint(int(len(r1)/2), len(r1) - 1)]

        childs_arr = []

        for i in range(len(r1)):
            childs_arr.append(0)

        for i in range(indices[1] - indices[0]):

            childs_arr[i + indices[0]] = r1[i + indices[0]]

        for i in range(len(r2)):

            if r2[i] not in childs_arr:
                
                childs_arr[childs_arr.index(0)] = r2[i]
            
        child = ''.join(childs_arr)

        return Road(child, "PMX")

def run():

    curr = Finder()

    curr.rank()

    gen_count = 0

    mut_rat = MUTATION_RATE

    time_since_last_usurp = 0
    current_record = 9999

    while True:
        curr.generate_children(mut_rat)

        gen_count += 1

        curr.rank()

        if curr.roads[0].length < current_record:

            time_since_last_usurp = 0

            mut_rat = MUTATION_RATE

            current_record = curr.roads[0].length

        else:

            time_since_last_usurp += 1


        if(time_since_last_usurp % 50 == 0 and time_since_last_usurp != 0):
            

            if POPULATION_SIZE - mut_rat > 20:

                mut_rat = int((2 * POPULATION_SIZE + mut_rat) / 3)
            
            else:

                winner = curr.roads[0]

                print(f"Top performer of this runn is 'A{winner.trip}A' with a length of {winner.length}. It was born via {winner.type}")
                # print(f"It will now be saved, and in the future it will be included in all starting pools.")

                # with open("GA for IBCSY2/winners.txt", 'a') as f:

                #     f.write(f"{winner.trip}\n")

                #     f.close()
                
                break


        print(f"Top performer of Generation {gen_count} is '{curr.roads[0].trip}' with a length of {curr.roads[0].length}. It was born via {curr.roads[0].type}")

        print(time_since_last_usurp)
        print(mut_rat)

        if gen_count > 199:
            break

if __name__ == '__main__':

    for i in range(1):

        with cProfile.Profile() as pr:
            run()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="GA for IBCSY2/stats.prof")

"""
FRI26 is a set of 26 cities, from TSPLIB. The minimal tour has length 937.

fri26.tsp, the TSP specification of the data.
fri26_d.txt, the intercity distance table.
fri26_s.txt, an itinerary that minimizes the total distance.



BCDFEGHIJNOMLKPSTRQUVZWXY
BCDFEGHIJNOMLKPSTRQUVZWXY
"""