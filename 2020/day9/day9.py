import itertools
import operator
import functools
import sys

sys.path.append('../..')

import utils

test_data = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

def find_unique(data):
    for end in range(25, len(data)):
        result = [seq for seq in itertools.combinations(data[end-25:end], 2) if sum(seq) == data[end]]
        if not result:
            return (data[end])

def find_weakness(data, num):
    for start in range(0, len(data)): 
        for val in itertools.accumulate(data[start:], operator.add):
            if val == num:
                start_loc = start
                while val > 0:
                    start += 1
                    val -= data[start]
                weakness = min(data[start_loc:start]) + max(data[start_loc:start])
                return weakness

            if val > num:
                break


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()
 
    # data = test_data.split("\n")
    data = list(map(int, data))
    unique = find_unique(data)
    print(unique)
    weakness = find_weakness(data, unique)
    print(weakness)

