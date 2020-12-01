import itertools
import operator
import functools
import sys

sys.path.append('../..')

import utils

# takes input and finds the two numbers that
# add up to 2020

@utils.func_timer
def part1(data, n):
    for i in itertools.combinations(data, n):
        if sum(i) == 2020:
            val = functools.reduce(operator.mul, i)
            print (val)
            break

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()

    data = list(map(int, data))
    part1(data, 2)
    part1(data, 3)
