from aocd.models import Puzzle
import re

puzzle = Puzzle(2024, 3)
input = puzzle.input_data
# input = puzzle.examples[0].input_data

def get_string_total(s):
	results = re.findall(r'mul\(\d+\,\d+\)', s)

	total = 0;
	for r in results:
		vals = list(map(int, re.findall(r'\d+', r)))
		total += (vals[0] * vals[1])

	return total

print(get_string_total(input))

# input = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

total = 0
current = 0
enabled = True
while (current < len(input)):
	if enabled == True:	
		end = input[current:].find("don't")
		if (end != -1):
			slice = input[current:current+end]
			end += 5
		else:
			slice = input[current:]
			end = len(input)

		total += get_string_total(slice)
		enabled = False

	else:
		end = input[current:].find("do")
		if end != -1:
			# mnake sure to skip any other don'ts in the list
			if input[current+end:current+end+5] != "don't":
				enabled = True
				end += 2
			else:
				end += 5

	current += end

print(total)

			
