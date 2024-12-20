from aocd.models import Puzzle
from collections import deque, Counter

puzzle = Puzzle(2024, 12)
# input = puzzle.input_data.splitlines()
input = puzzle.examples[0].input_data.splitlines()
# input = """AAAAAA
# AAABBA
# AAABBA
# ABBAAA
# ABBAAA
# AAAAAA""".splitlines()

# input = """EEEEE
# EXXXX
# EEEEE
# EXXXX
# EEEEE""".splitlines()

# input = """RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE""".splitlines()

# input = """AABB
# AABB
# BBAA
# BBAA""".splitlines()

map = {complex(j,i): c for i,r in enumerate(input) for j,c in enumerate(r.strip())}
dirs = [ complex (0, -1), complex(1, 0), complex(0,1), complex(-1, 0) ]
# corner_dirs = [ complex(-1, -1), complex(-1, 1), complex(1, -1), complex(1, 1)]

corner_dirs = [ (complex(0, -1), complex(-1, 0)), (complex(0, -1), complex(1, 0)),
			   (complex(0, 1), complex(-1,0)), (complex(0, 1), complex(1, 0)) ]

vals = set([c for c in map.values()])

def flood_fill(start, map):

	visited = set() 
	q = deque( [start] )

	while len(q) > 0:
		v = q.pop()
		if v not in visited:
			visited.add(v)

			for d in dirs:
				v1 = d + v
				if v1 in map and map[v1] == map[start]:
					q.append( v1 )

	return visited


def find_areas(map, c):
	areas = []
	positions = set([l for l,p in map.items() if p == c])
	while len(positions):
		p = positions.pop()
		a = flood_fill(p, map)
		areas.append(a)
		positions -= a

	return areas

price = 0
price2 = 0
for v in vals:
	plots = find_areas(map, v)
	for plot in plots:
		area = len(plot)
		perimeter = []
		for x in plot:
			for d in dirs:
				p1 = x + d
				if p1 not in map or map[p1] != map[x]:
					perimeter.append(p1)

		# with perimeter calculated, find all the corners
		# corners = 0
		# for s in perimeter:
		# 	for d in corner_dirs:
		# 		s1 = s + d
		# 		if s1 in perimeter:
		# 			s2 = s + complex(0, d.imag)
		# 			s3 = s + complex(d.real, 0)
		# 			if (s2 in p and map[s2] == v) or (s3 in p and map[s3] == v):
		# 				corners += 1
		
		corners = 0
		summ = 0
		for p in plot:
			l = [ map[p+d] if p+d in map else None for d in dirs ]
			summ += sum( [1 if p+d in perimeter else 0 for d in dirs] )
			corners += sum( x != v for x in l )

		price += (area * len(perimeter))
		price2 += (area * (corners))

print(price, price2)
