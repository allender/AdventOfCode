import sys
from collections import Counter
from collections import defaultdict

sys.path.append('../..')

import utils

test_data = """16
10
15
5
1
11
7
19
6
12
4"""

test_data2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()
 
    data = list(map(int, data))
    data.sort()
    data.append(data[-1] + 3)
    data.insert(0, 0)
    diff_counter = Counter( [ data[i] - data[i-1] for i in range(len(data)) ] )
    print(diff_counter[1], diff_counter[3], diff_counter[1] * diff_counter[3])

    num_paths = defaultdict(int)
    num_paths[0] = 1
    for j in data[1:]:
        num_paths[j] = num_paths[j-1] + num_paths[j-2] + num_paths[j-3]
    print(num_paths[max(data)])