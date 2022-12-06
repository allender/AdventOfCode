from aocd.models import Puzzle
from aocd import lines

puzzle = Puzzle(year=2022, day = 4)

num_overlapping = 0
num_overlapping_at_all = 0
for l in lines:
    first,second = (list(map(int,a.split('-'))) for a in l.split(','))
    set1 = set(range(first[0], first[1] + 1))
    set2 = set(range(second[0], second[1] + 1))

    if set1.issubset(set2) or set2.issubset(set1):
        num_overlapping += 1

    if set1.intersection(set2):
        num_overlapping_at_all += 1

print(num_overlapping)
print(num_overlapping_at_all)