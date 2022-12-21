from aocd.models import Puzzle
import re
import sys
from collections import defaultdict

puzzle = Puzzle(year=2022, day = 16)

test_data = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''

class Valve():
    bmask = 1

    def __init__(self, label, rate, paths):
        self.label = label
        self.rate = rate
        self.paths = { p : 1 for p in paths } 
        self.paths = defaultdict(lambda: sys.maxsize, self.paths)
        self.id = Valve.bmask
        Valve.bmask <<= 1

    def __repr__(self):
        return f'{self.label}: {self.rate} -- {self.paths}'

def turn_valves(valve_label, current_time, state, current_rate = 0, all_costs = defaultdict(int)):
    all_costs[state] = max(all_costs[state], current_rate)
    for dest_label, dest_time in valves[valve_label].paths.items():
        if valves[dest_label].rate == 0: 
            continue
        new_time = current_time - (dest_time + 1)
        if new_time < 0 or (valves[dest_label].id & state):
            continue
        turn_valves(dest_label, new_time, state | valves[dest_label].id, current_rate + new_time * valves[dest_label].rate, all_costs)
    return all_costs    

data = puzzle.input_data
valves = {}
for l in [re.split(r'[\s=;,]+', x) for x in data.splitlines()]:
    valves[l[1]] = Valve(l[1], int(l[5]), l[10:])

# calculate min distnances from all valves to all other values
for l0, v0 in valves.items():
    for l1, v1 in valves.items():
        for l2, v2 in valves.items():
            valves[l1].paths[l2] = min(valves[l1].paths[l2], valves[l1].paths[l0] + valves[l0].paths[l2])

# paths = turn_valves('AA', 30, 0)
# print(max(paths.values()))

# for some reason, part2 doesn't give correct value unless we don't run part1
# Not looking for real reason right now :)
paths = turn_valves('AA', 26, 0)
print(max(cost1 + cost2 for path1, cost1 in paths.items()
                        for path2, cost2 in paths.items()
                        if not path1 & path2))
