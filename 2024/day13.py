from aocd.models import Puzzle
import re

puzzle = Puzzle(2024, 13)
input = puzzle.input_data.splitlines()
# input = puzzle.examples[0].input_data.splitlines()

def solve(part2 = False):
	total = 0
	for i in range((len(input)+1) // 4):
		x1, y1 = map(int, re.findall(r'(\d+)', input[i*4]))
		x2, y2 = map(int, re.findall(r'(\d+)', input[i*4+1]))
		tx, ty = map(int, re.findall(r'(\d+)', input[i*4+2]))

		if part2 == True:
			tx += 10000000000000
			ty += 10000000000000

		b, br = divmod((tx * y1 - ty  * x1), (x2 * y1 - x1 * y2))
		a, ar = divmod((tx - b * x2), x1)

		if b < 0 or a < 0:
			continue

		if ar or br:
			continue

		if part2 == False and (b > 100 or a > 100):
			continue

		total += 3 * a + b

	return total

print(solve())
print(solve(True))

