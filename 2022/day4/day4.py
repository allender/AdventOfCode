from aocd.models import Puzzle
from aocd import lines

puzzle = Puzzle(year=2022, day = 4)

num_overlapping = 0
num_overlapping_at_all = 0
for l in lines:
    first,second = (list(map(int,a.split('-'))) for a in l.split(','))

    # are teh complete ranges overlapping
    if (second[0] >= first[0] and second[1] <= first[1]) or (first[0] >= second[0] and first[1] <= second[1]):
        num_overlapping = num_overlapping + 1

    # is there any overlap at all
    if (second[0] >= first[0] and second[0] <= first[1]) or (second[1] >= first[0] and second[1] <= first[1]) or (first[0] >= second[0] and first[0] <= second[1]) or (first[1] >= second[0] and first[1] <= second[1]):
        num_overlapping_at_all += 1

print(num_overlapping)
print(num_overlapping_at_all)