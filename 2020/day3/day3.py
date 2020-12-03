import itertools
import operator
import functools
from collections import namedtuple
import re
import sys

sys.path.append('../..')

import utils

Point = namedtuple('Point', ['x', 'y'])
Slope = namedtuple('Slope', ['x', 'y'])

def get_num_trees(data, slope):
    num_rows = len(data)
    num_cols = len(data[0])
    cur_loc = Point(0,0)

    # loop through until we get to the bottom
    num_trees = 0
    while cur_loc.y < num_rows - 1:
        cur_loc = Point((cur_loc.x + slope.x) % num_cols, cur_loc.y + slope.y)

        if data[cur_loc.y][cur_loc.x] == '#':
            num_trees = num_trees + 1

    return num_trees


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()

    print (get_num_trees(data, Slope(3, 1)))

    slopes = []
    slopes.append(Slope(1, 1))
    slopes.append(Slope(3, 1))
    slopes.append(Slope(5, 1))
    slopes.append(Slope(7, 1))
    slopes.append(Slope(1, 2))

    val = 1
    for slope in slopes:
        val *= get_num_trees(data, slope)

    print (val)