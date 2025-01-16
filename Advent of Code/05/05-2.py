import re
from concurrent.futures import ThreadPoolExecutor

def convert_number(number, maps):
    for map_ in reversed(maps):
        destination_start, source_start, length = map_
        if source_start <= number < source_start + length:
            return destination_start + (number - source_start)
    return number

def find_lowest_location_worker(args):
    num, map_ = args
    return convert_number(num, map_)

def find_lowest_location(seeds, maps):
    current_numbers = seeds

    with ThreadPoolExecutor() as executor:
        for map_ in maps:
            args_list = [(num, map_) for num in current_numbers]
            current_numbers = list(executor.map(find_lowest_location_worker, args_list))

    return min(current_numbers)

def extract_seed_ranges(input_string):
    seeds_match = re.search(r"seeds: (.+)", input_string)
    seed_ranges = list(map(int, seeds_match.group(1).split()))
    
    seeds = []
    for i in range(0, len(seed_ranges), 2):
        start = seed_ranges[i]
        length = seed_ranges[i + 1]
        seeds.extend(range(start, start + length))

    return seeds


with open("05/input.txt", "r") as f:
    strin = f.read()

    # Extract seeds
    seeds = extract_seed_ranges(strin)

    # Extract maps
    map_matches = re.finditer(r"(\w+-to-\w+ map:.*?(\d+ \d+ \d+)(?:.*?(?=\w+-to-\w+ map:|$)))", strin, re.DOTALL)
    maps = []
    for match in map_matches:
        map_data = match.group(1)
        map_lines = map_data.split('\n')[1:-1]  # Exclude the map name and the empty line
        map_tuples = [tuple(map(int, line.split())) for line in map_lines]
        maps.append(map_tuples)
    
    maps = [[tpl for tpl in m if tpl] for m in maps]

    # print("Seeds:", seeds)
    # print("Maps:", maps)

    lowest_location = find_lowest_location(seeds, maps)
    print(f"The lowest location number is: {lowest_location}")

    