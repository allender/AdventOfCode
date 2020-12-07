import itertools
import operator
import functools
from collections import namedtuple
import re
import sys

sys.path.append('../..')

import utils

test_data = """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL"""

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read()

    data = data.split('\n')

    highest = 0
    seats_taken = []
    for p in data:
        row = sum([ 1 << (6 - index) if b == 'B' else 0 for index, b in enumerate(p[0:7]) ])
        col = sum([ 1 << (2 - index) if b == 'R' else 0 for index, b in enumerate(p[7:10]) ])

        id = (row * 8) + col
        if (id > highest):
            highest = id
        seats_taken.append(id)

    l = list(range(0,highest))
    for s in seats_taken:
        if s in l:
            l.remove(s)

    print(l)
        
 