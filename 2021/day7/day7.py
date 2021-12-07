from aocd import lines
from collections import defaultdict
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

# sum consecutive numbers 1 through n
def summation(n):
    return int((n / 2) * (1 + n))

def part2(positions: List):
    smallest = min(positions)
    largest = max(positions)

    fuel_used = []
    for i in range(smallest, largest + 1):
        fuel = 0
        for j in positions:
            fuel += summation(abs(j-i))
        fuel_used.append(fuel)

    return min(fuel_used)

            
if __name__ == '__main__': 
    numbers = list(map(int, lines[0].split(',')))

    print(part1(numbers))
    print(part2(numbers))
