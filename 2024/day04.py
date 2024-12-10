from aocd.models import Puzzle
from collections import defaultdict

puzzle = Puzzle(2024, 4)
input = puzzle.input_data.splitlines()
# input = puzzle.examples[0].input_data.splitlines()
# input = """MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX """.splitlines()

grid = { (x, y): c for y, l in enumerate(input) for x, c in enumerate(l)}

dirs = ((1, 0), (-1,0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
ddirs = ((-1, -1), (-1, 1), (1, -1), (1, 1))

xmas = 'XMAS'
mas = 'MAS'

def find_word(grid, x, y, dir, word, index):
	new_x = x + d[0]
	new_y = y + d[1]
	if new_x < 0 or new_y < 0 or new_x >= len(input[0]) or new_y >= len(input):
		return 0

	if grid[(new_x, new_y)] == word[index]:
		if index == len(word) - 1:
			return 1

		return find_word(grid, new_x, new_y, dir, word, index + 1)
		
	return 0
	
count = 0
for y in range(len(input)):
	for x in range(len(input[0])):
		if grid[(x,y)] == 'X':
			for d in dirs:
				count += find_word(grid, x, y, d, 'XMAS', 1)

print(count)

count = 0
amap = defaultdict(int)
for y in range(len(input)):
	for x in range(len(input[0])):
		if grid[(x,y)] == 'M':
			for d in ddirs:
				found = find_word(grid, x, y, d, 'MAS', 1)
				if found == 1:
					amap[(x + d[0], y + d[1])] += 1
				count += found


print(sum(1 for k,v in amap.items() if v == 2))