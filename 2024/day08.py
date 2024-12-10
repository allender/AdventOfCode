from aocd.models import Puzzle
from collections import defaultdict
from itertools import permutations, product

puzzle = Puzzle(2024, 8)
input = puzzle.input_data.splitlines()
# input = puzzle.examples[0].input_data.splitlines()
# input = """T....#....
# ...T......
# .T....#...
# .........#
# ..#.......
# ..........
# ...#......
# ..........
# ....#.....
# ..........""".splitlines()

map = {complex(j,i): c for i,r in enumerate(input) for j,c in enumerate(r.strip())}
ant = defaultdict(list)
for k,v in map.items():
	if v != '.' and v != '#':
		ant[v].append(k)

antia = defaultdict(list) 
for k,v in ant.items():
	for pair in permutations(v, 2):
		d1 = pair[0] - pair[1]
		p = pair[0] + d1
		if p in map:
			antia[p].append('#')

		p = pair[1] - d1
		if p in map:
			antia[p].append('#')

print(len(antia))

antia = defaultdict(list) 
for k,v in ant.items():
	for pair in permutations(v, 2):
		d1 = pair[0] - pair[1]
		antia[pair[0]].append('#')
		antia[pair[1]].append('#')
		p = pair[0] + d1
		while p in map:
			antia[p].append('#')
			p +=  d1

		p = pair[1] - d1
		while p in map:
			antia[p].append('#')
			p -= d1


print(len(antia))