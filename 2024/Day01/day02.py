from aocd.models import Puzzle

puzzle = Puzzle(2024, 2)
lines = [ list(map(int, l.split(' '))) for l in puzzle.input_data.splitlines() ]
# lines = [ list(map(int, l.split(' '))) for l in puzzle.examples[0].input_data.splitlines() ]

def issafe(level):
	diffs = list(map(lambda x: x[1] - x[0], zip(level[:-1], level[1:])))
	dset = set(diffs)
	if dset.issubset({1, 2, 3}) or dset.issubset({-1, -2, -3}):
		return 1
	return 0

def issafe2(level):
	if issafe(level) == 1:
		return 1

	if any(issafe(level[:i] + level[i+1:]) for i in range(len(level))):
		return 1
	return 0

numsafe = sum(issafe(l) for l in lines)
numsafe2 = sum(issafe2(l) for l in lines)	

print(numsafe)
print(numsafe2)
