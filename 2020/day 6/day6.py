import re
import sys
import collections

sys.path.append('../..')

import utils

test_data = """abc

a
b
c

ab
ac

a
a
a
a

b"""

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read()

    data = data.split('\n\n')

    any_yes = 0
    all_yes = 0
    for group in data:

        split_group = group.replace('\n','')
        any_yes += len(set(split_group))

        count_dict = collections.Counter(split_group)
        print(count_dict)
        all_yes += sum( [x == len(group.split('\n')) for x in count_dict.values()] )

    print (any_yes, all_yes)
