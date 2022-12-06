from aocd.models import Puzzle
from aocd import lines

puzzle = Puzzle(year=2022, day = 6)

data = puzzle.input_data

def find_marker(s, l):
    lists = [ s[i:i+l] for i in range(len(s))]
    for index, list in enumerate(lists):
        count = set(list)
        if len(count) == l:
            return index + l
    return -1

print(find_marker(data, 4))
print(find_marker(data,14))