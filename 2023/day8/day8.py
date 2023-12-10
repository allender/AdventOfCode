from aocd.models import Puzzle
import itertools
from math import lcm

puzzle = Puzzle(2023, 8)

example2 = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''

input = puzzle.input_data.split('\n\n')
# input = puzzle.examples[0][0].split('\n\n')
# input = example2.split('\n\n')

mappings={}
dirs = [ 1 if x == 'R' else 0 for x in input[0] ]
for l in input[1].splitlines():
    key = l.split()[0]
    values = l.split('=')[1].strip()
    mappings[key] = [ x.strip('() ') for x in values.split(',')]


def solve(node, part1 = False):
    # iterator to cycle through input
    cycle = itertools.cycle(dirs)

    num_steps = 0
    while True:
        num_steps += 1
        c = next(cycle)
        val = mappings[node][c]

        if part1 == True and val == 'ZZZ':
            break

        elif part1 == False and val[2] == 'Z':
            break

        node = val

    return num_steps

print(solve('AAA', True))

# part two get all of the nodes ending with A
starts = [ x for x in mappings.keys() if x[2] == 'A' ]
totals = [ solve(s, False) for s in starts ]
print(lcm(*totals))


