from aocd.models import Puzzle
from collections import defaultdict


puzzle = Puzzle(2024, 6)
input = puzzle.input_data.splitlines()
# input = puzzle.examples[0].input_data.splitlines()

maze = {complex(j,i): c for i,r in enumerate(input) for j,c in enumerate(r.strip())}
start = [l for l,p in maze.items() if p == '^']
dirs = [ complex (0, -1), complex(1, 0), complex(0,1), complex(-1, 0) ]

d = dirs[0]
current = start[0]
visited = {current} 
while (current + d in maze):
	new_position = current + d
	if maze[new_position] == '#':
		d = dirs[(dirs.index(d) + 1) % len(dirs)]
	else:
		visited.add(new_position)
		current = new_position

print(len(visited))

# brute force 
num_found = 0
for p in visited - {start[0]}:
	maze[p] = '#'
	d = dirs[0]
	current = start[0]
	seen = { (current, d) }
	while (current + d in maze and (current + d, d) not in seen):
		new_position = current + d
		if maze[new_position] == '#':
			d = dirs[(dirs.index(d) + 1) % len(dirs)]
		else:
			seen.add((new_position, d))
			current = new_position

	maze[p] = '.'
	if (current+d, d) in seen:
		num_found += 1

print(num_found)