from aocd.models import Puzzle
from aocd import lines
from itertools import groupby

puzzle = Puzzle(year=2022, day =1)

counts = []
calcount = 0
for l in lines:
    if l == '':
        counts.append(calcount)
        calcount = 0
    else:
        calcount += int(l)

counts = sorted(counts)
print(counts[-1])
print(sum(counts[-3:]))