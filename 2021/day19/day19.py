from dataclasses import dataclass
from typing import List
from itertools import permutations

class Point():
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def distsq(self, point):
		return (self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2

	def __sub__(self, point):
		return Point(self.x - point.x, self.y - point.y, self.z - point.x)

	def __add__(self, point):
		return Point(self.x + point.x, self.y + point.y, self.z + point.x)

	def __str__(self):
		return f'({self.x}, {self.y}, {self.z})'

	def __repr__(self):
		return self.__str__()

class Scanner():
	id = 0
	axis_iter = permutations(range(3))

	def __init__(self, _points: List[Point]):
		self.id = Scanner.id
		Scanner.id += 1

		# where the scanner is located
		self.center = Point(0, 0, 0)
		# list of points that this scanner sees
		self.points = _points

		# dictionary of distances from one beacon to all other beacons
		self.distances = {} 
		for p in self.points:
			self.distances[p] = [ p.distsq(x) for x in self.points if x != p ]

	def __str__(self):
		return f'{self.id} - # points: {len(self.points)}'

	def __repr__(self):
		return self.__str__()

	def find_overlapping_points(self, s : 'Scanner'):
		p1_list = []
		p2_list = []
		for p1, d1 in self.distances.items():
			for p2, d2 in s.distances.items():
				total = sum([ 1 for x in d2 if x in d1 ])

				# if there are 11 (plus 1 for the current point which is 12)
				# then we have a set of common points so add to lists
				# and then we will calculate actual point locations
				if total == 11:
					p1_list.append(p1)
					p2_list.append(p2)

		if len(p1_list) > 0:
			print (p1_list, p2_list)


def parse_scanners(filename: str) -> List[Scanner]:
	scanners = []
	with open(filename) as f:
		scanner_points = [ [ c for c in line.strip('\n').split('\n') ] for line in f.read().split('\n\n')]
		for sp in scanner_points:
			points = []
			for p in sp[1:]:
				x, y, z = [ int(v) for v in p.split(',') ]
				points.append(Point(x, y, z))

			scanners.append(Scanner(points))

	return scanners

def part1(scanners: List[Scanner]) -> int:
	# pull off the first scanner (0) and calculate the distances
	# from point to scanner (which we arbitrarily put at 0,0,0)
	cur_scanner = scanners.pop(0)
	processed_scanners = [ cur_scanner ]

	# for the rest of the scanners, identify the points in 
	# common and put them into the scanner's list of points
	next_scanner = scanners.pop(0)
	for s in processed_scanners:
		s.find_overlapping_points(next_scanner)

	return 0

if __name__ == '__main__':
	scanners = parse_scanners('test.txt')
	print(scanners)
	print(part1(scanners))
