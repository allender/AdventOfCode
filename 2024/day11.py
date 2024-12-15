from aocd.models import Puzzle
from collections import deque

puzzle = Puzzle(2024, 11)
input = puzzle.input_data.split(" ")
# input = puzzle.examples[0].input_data
# input = "125 17"
stones = [ int(i) for i in input ]

cache = {}

def newstones(steps, stone):
	if (stone,steps) in cache:
		return cache[(stone, steps)]
	
	if steps == 0:
		return 1
	
	if stone == 0:
		return newstones(steps-1, 1)
	

	ss = str(stone)
	if len(ss)%2 == 0:
		s1, s2 = int(ss[:len(ss)//2]), int(ss[len(ss)//2:])
		total = newstones(steps - 1, s1) + newstones(steps - 1, s2)
		cache[(stone, steps)] = total
		return total

	return newstones(steps - 1, stone * 2024)

print(sum([newstones(25, i) for i in stones]))
print(sum([newstones(75, i) for i in stones]))
