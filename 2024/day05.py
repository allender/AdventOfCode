from aocd.models import Puzzle
from collections import defaultdict

puzzle = Puzzle(2024, 5)
input = puzzle.input_data.split('\n\n')
# input = puzzle.examples[0].input_data.split('\n\n')
orderings = defaultdict(list)
for l in input[0].splitlines():
	x, y = l.split('|')
	orderings[int(x)].append(int(y))

manuals = [ list(map(int, l.split(',')))  for l in input[1].splitlines() ]

sum = 0
sum2 = 0
for m in manuals:
	sorted_pages = sorted(m, key = lambda page: -len([x for x in orderings[page] if x in m]))
	if m == sorted_pages:
		sum += m[len(m)//2]
	else:
		sum2 += sorted_pages[len(m)//2]


print(sum, sum2)