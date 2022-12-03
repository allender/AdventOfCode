from aocd.models import Puzzle
from aocd import lines
from collections import defaultdict
from itertools import groupby

puzzle = Puzzle(year=2022, day = 3)

def get_score(c):
    if ord(c) >= ord('a'):
        return ord(c) - ord('a') + 1
    return ord(c) - ord('A') + 27

sacks = []
score = 0
for line in lines:
    half = len(line) // 2
    first = line[:half]
    second = line[half:]
    sacks.append((first, second))
    common = [ c for c in first if c in second ]
    score += get_score(common[0])

print(score)

size = 3
score = 0
groups = [ lines[n:n+size] for n in range(0, len(lines), size)]
for group in groups:
    d = defaultdict(int)
    for g in group:
        g = sorted(g)
        for k, _ in groupby(g):
            d[k] =d[k] + 1

    for k,v in d.items():
        if v == 3:
            score += get_score(k)
            break

print(score)

    