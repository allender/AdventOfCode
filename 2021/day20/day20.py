from aocd import lines
from dataclasses import dataclass
from typing import List, Tuple
from collections import defaultdict

test_lines = [
	'..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#',
	'',
	'#..#.',
	'#....',
	'##..#',
	'..#..',
	'..###',
]

offsets = [ (-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

def print_grid(grid):
	(minx, maxx), (miny, maxy) = ((min(x), max(x)) for x in zip(*grid))
	for y in range(miny, maxy + 1):
		for x in range(minx, maxx + 1):
			if (x, y) in grid:
				print('#', end='')
			else:
				print('.', end='')
		print('')
	print('')


def process_grid(grid, mapping, iteration):
	cur_map = mapping[iteration % len(mapping)]
	new_grid = set()
	(minx, maxx), (miny, maxy) = ((min(x), max(x)) for x in zip(*grid))
	for y in range(miny - 1, maxy + 2):
		for x in range(minx - 1, maxx + 2):
			value = 0
			point = (x, y)
			for new_point in [(x + x1, y + y1) for (x1, y1) in offsets]:
				value = value << 1
				if new_point in grid:
					value += 1

			if value in cur_map:
				new_grid.add(point)

	return new_grid

def parse_input(lines):
	mapping_string = lines[0]

	# array of mappings.  One for if zero maps to 0 (in which case it's all 0's to infinity),
	# and one for when 0's map to 1s (but assert that 1's map to 0).
	if mapping_string[0] == '.':
		mapping = [ [i for i, c in enumerate(mapping_string) if c == '#'] ]
	else:
		assert(mapping_string[-1] == '.')
		mapping = [ [i for i, c in enumerate(mapping_string) if c == '.'],
					[i ^ 511 for i, c in enumerate(mapping_string) if c == '#'] ]
		
	grid = { (x, y) for y, l in enumerate(lines[1:]) for x, c in enumerate(l) if c == '#' }

	return mapping, grid

if __name__ == '__main__':
	mapping, grid = parse_input(lines)
	for i in range(50):
		grid = process_grid(grid, mapping, i)

	print(len(grid))
