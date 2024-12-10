from aocd.models import Puzzle
from functools import reduce

puzzle = Puzzle(2024, 7)
input = puzzle.input_data.splitlines()
# input = puzzle.examples[0].input_data.splitlines()

def is_valid(total, numbers, concatenate = False):

	running_totals = {total}
	while len(numbers) > 0:
		last = numbers.pop()
		new_totals = set()
		for n in running_totals:
			prev = n - last
			if prev >= 0:
				new_totals.add(prev)

			if n >= last and n % last == 0:
				new_totals.add(n // last)

			if concatenate == True:
				x = last
				valid = True
				while x > 0:
					if x % 10 == n % 10:
						n //= 10
						x //= 10
					else:
						valid = False
						break
				if valid == True:
					new_totals.add(n)
		

		running_totals = new_totals


	if 0 in running_totals:
		return True
	return False

calibration1 = 0
calibration2 = 0
for i in input:
	total, s = i.split(':')
	total = int(total)
	numbers = list(map(int, [x for x in s.strip().split(' ')]))
	if is_valid(total, numbers):
		calibration1 += total
	numbers = list(map(int, [x for x in s.strip().split(' ')]))
	if is_valid(total, numbers, True):
		calibration2 += total

print (calibration1)
print (calibration2)
