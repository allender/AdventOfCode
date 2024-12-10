from aocd.models import Puzzle
from collections import defaultdict
import heapq

puzzle = Puzzle(2024, 9)
input = puzzle.input_data
# input = puzzle.examples[0].input_data

# lengths = [ int(i) for i in input ]
# grid = [ i//2 if i%2 == 0 else -1 for i,num in enumerate(lengths) for _ in range(num) ]

# while -1 in grid:
# 	if grid[-1] == -1:
# 		grid.pop()
# 	else:
# 		index = grid.index(-1)
# 		grid[index] = grid.pop()

# x = sum(i * num for i,num in enumerate(grid))

lengths = [ (i//2 if i%2 else -1, int(v)) for i,v in enumerate(input, 1) ]
for i in range(len(lengths))[::-1]:
	for j in range(i):
		d1, s1 = lengths[i]
		d2, s2 = lengths[j]
		if d1 >= 0 and d2 == -1 and s1 <= s2:
			lengths[i] = (-1, s1)
			lengths[j] = (-1, s2 - s1)
			lengths.insert(j, (d1, s1))

flatten = lambda x: [x for x in x for x in x]
flattened = flatten([d]*s for d,s in lengths)

print(sum((i*(c) for i,c in enumerate(flattened) if c != -1)))