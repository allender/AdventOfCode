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
    end = data.index(num)
    for start in range(0, end): 
        result = [ i for i, val in enumerate(itertools.accumulate(data[start:end], operator.add)) if val == num ]
        if result:
            return (min(data[start:start+result[0]]) + max(data[start:start+result[0]]))

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()
 
    # data = test_data.split("\n")
    data = list(map(int, data))
    unique = find_unique(data)
    print(unique)
    weakness = find_weakness(data, unique)
    print(weakness)

