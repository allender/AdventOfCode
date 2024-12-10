from aocd.models import Puzzle
from collections import deque

puzzle = Puzzle(2024, 10)
input = puzzle.input_data.splitlines()
# input = puzzle.examples[0].input_data.splitlines()

map = {complex(j,i): int(c) if c != '.' else -1 for i,r in enumerate(input) for j,c in enumerate(r.strip())}
start = [l for l,p in map.items() if p == 0]
dirs = [ complex (0, -1), complex(1, 0), complex(0,1), complex(-1, 0) ]

def dfs_search(map, start, part2 = False):
	count = 0
	for s in start:
		visited = set() 
		q = deque( [s] )

		while len(q) > 0:
			v = q.pop()
			current = map[v]

			if part2 == True or v not in visited:
				visited.add(v)

				if current == 9:
					count += 1

				for d in dirs:
					v1 = d + v
					if v1 in map and map[v1] == current + 1:
						q.append( v1 )
	return count

print(dfs_search(map, start))
print(dfs_search(map, start, True))
