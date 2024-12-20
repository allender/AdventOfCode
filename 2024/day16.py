from aocd.models import Puzzle
import heapq


puzzle = Puzzle(2024, 16)
# input = puzzle.input_data
input = puzzle.examples[0].input_data.splitlines()

maze = {complex(j,i): c for i,r in enumerate(input) for j,c in enumerate(r.strip())}
start = [ v for v,k in maze.items() if k == 'S'][0]
end = [ v for v,k in maze.items() if k == 'E'][0]
dirs = [ complex (0, -1), complex(1, 0), complex(0,1), complex(-1, 0) ]
print(start,end)

def search(maze, start):
	visited = set()
	q = [(0, start, dirs[1], {start})]
	while len(q) > 0:
		dist, v, direction, path = heapq.heappop(q)
		if v in visited:
			continue
		visited.add(v)

		if v == end:
			return d, path
		
		for d in dirs:
			if d.real == -direction.real and d.imag == -direction.imag:
				continue
			v1 = d + v
			if maze[v1] == '#' or v1 in visited:
				continue

			path1 = path.copy()
			path1.add(v1)
			heapq.heappush(q, (dist + 1, v1, d, path1))

	assert(0)


search(maze, start)