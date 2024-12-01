from aocd.models import Puzzle

puzzle = Puzzle(2024, 1)
lines = [ list(map(int, l.split('   '))) for l in puzzle.input_data.splitlines() ] 
# lines = [ list(map(int, l.split('   '))) for l in puzzle.examples[0].input_data.splitlines() ] 
set1, set2 = map(sorted, map(list, zip(*lines)))

diff_sum = sum(list(map(lambda x,y : abs(x -y), set1, set2)))

print(diff_sum)

total = 0
for x in set1:
	total += (x * set2.count(x))

print(total)
	