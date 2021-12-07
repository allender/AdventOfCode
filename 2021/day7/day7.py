from aocd import lines
from collections import Counter
from typing import List

test_lines = [
    '16,1,2,0,4,2,7,1,2,14'
]

def part1(positions : List):
    smallest = min(positions)
    largest = max(positions)
    fuel_used = []
    for i in range(smallest, largest + 1):
        fuel = sum( [ abs(j - i) for j in positions ] )
        fuel_used.append(fuel)

    return min(fuel_used)

def part2(positions: List):
    smallest = min(positions)
    largest = max(positions)
    fuel_used = []

    for i in range(smallest, largest + 1):
        fuel = 0
        for j in positions:
            fuel += sum( [x for x in range(abs(j - i) + 1) ])
        fuel_used.append(fuel)

    return min(fuel_used)

            
if __name__ == '__main__': 
    numbers = list(map(int, lines[0].split(',')))

    print(part1(numbers))
    print(part2(numbers))
