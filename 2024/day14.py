from aocd.models import Puzzle
from collections import defaultdict
import math
import re


puzzle = Puzzle(2024, 14)
input = puzzle.input_data.splitlines()
WIDTH = 101
HEIGHT = 103
# input = puzzle.examples[0].input_data.splitlines()
# WIDTH = 11
# HEIGHT = 7
xmid = WIDTH//2
ymid = HEIGHT//2

def parse():
	robots = []
	num_robots = 0
	for i in input:
		num_robots += 1
		x, y, dx, dy = list(map(int, re.findall(r'(-*\d+)', i)))
		assert(complex(dx, dy) not in robots)
		robots.append([complex(x, y), complex(dx, dy)])

	return num_robots, robots

def solve(robots):
	moved_robots = [ ]
	for pos, delta in robots:
		tmp = pos + delta
		new_point = complex(tmp.real % WIDTH, tmp.imag % HEIGHT)
		moved_robots.append([new_point, delta])

	return moved_robots

num_robots, robots = parse()
for _ in range(100):
	robots = solve(robots)

quads = defaultdict(int)
for pos, delts in robots:
	if (pos.real == xmid or pos.imag == ymid):
		continue
	quadx = 0 if (int(pos.real)) < xmid else 1
	quady = 0 if (int(pos.imag)) < ymid else 1
	assert(quadx in [0, 1] and quady in [0,1])
	quads[(quadx, quady)] += 1

print(math.prod(quads.values()))

num_robots, robots = parse()
for i in range(WIDTH * HEIGHT):
	robots = solve(robots)
	grid = defaultdict(int)
	for r in robots:
		grid[r[0]] += 1


	print(i)
	for y in range(HEIGHT):
		for x in range(WIDTH):
			if complex(x,y) in grid:
				print('#', end='')
			else:
				print('.', end='')

		print('')

	print('\n\n')
