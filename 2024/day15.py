from aocd.models import Puzzle
from collections import defaultdict
import math
import re


puzzle = Puzzle(2024, 15)
input = puzzle.input_data
# input = puzzle.examples[0].input_data

dir_map = {'^': complex(0, -1), 'v': complex(0, 1), '<': complex(-1, 0), '>': complex(1,0)}

# input = """########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# <^^>>>vv<v>>v<<"""

m, directions = input.split('\n\n')
map = {complex(j,i): c for i,l in enumerate(m.splitlines()) for j,c in enumerate(l.strip())}
width = len(m.splitlines()[0])
height = len(m.splitlines())
robot = [ x for x,v in map.items() if v == '@' ][0]

for d in directions:
	if d == '\n':
		continue
	pos = robot + dir_map[d] 
	assert pos in map
	if (map[pos] == '#'):
		continue
	if (map[pos] == '.'):
		map[robot] = '.'
		map[pos] = '@'
		robot = pos
		continue

	# deal with boxes
	assert(map[pos] == 'O')
	while(map[pos] == 'O'):
		pos = pos + dir_map[d]

	# if we are at a wall, do nothing
	if map[pos] == '#':
		continue

	# move the boxes
	while map[pos] != '@':
		map[pos] = 'O'
		pos -= dir_map[d]
	pos = pos + dir_map[d]
	map[pos] = '@'
	map[robot] = '.'
	robot = pos

for y in range(height):
	for x in range(width):
		print(map[complex(x, y)], end = '')
	print('')

print('')

s = sum((k.imag * 100 + k.real if v == 'O' else 0 for k,v in map.items()))

print(s)
		

