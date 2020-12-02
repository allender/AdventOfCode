import itertools
import operator
import functools
from collections import defaultdict
import re
import sys

sys.path.append('../..')

import utils

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()

    # compile regular expression for matching input
    part1_pass = 0
    part2_pass = 0
    exp = re.compile("(\d*)-(\d*) (\w): (\w*)")
    for line in data:
        m = exp.match(line)
        low = int(m.group(1))
        high = int(m.group(2))
        char = m.group(3)[0]
        pw = m.group(4)
        slots = defaultdict(int)
        specific_index = 0
        for index, c in enumerate(pw):
            slots[c] += 1
            if ((index == low - 1 or index == high - 1) and c == char):
                specific_index += 1

        if specific_index == 1:
            part2_pass += 1

        if (slots[char] >= low and slots[char] <= high):
            part1_pass += 1
            
    print (part1_pass, part2_pass)

