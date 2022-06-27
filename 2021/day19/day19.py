from re import I
from aocd import lines
from collections import namedtuple, defaultdict
from typing import List
from itertools import permutations, product, combinations

Point = namedtuple('Point', ['x', 'y', 'z'])

class Scanner():
	id = 0
	beacons = set()

	def __init__(self, _points: List[Point]):
		self.id = Scanner.id
		Scanner.id += 1

		# where the scanner is located
		self.center = Point(0, 0, 0)

		# list of points that this scanner sees
		self.points = _points

		# pre calculate all of the rotation values.   This is kind of
		# cheating and giving me 48 possible rotated points instead of 24, which is
		# all we need
		self.point_rotations = {}
		for p in self.points:
			self.point_rotations[p] = [ Point(p[x] * hx, p[y] * hy, p[z] * hz) for x, y, z in permutations(range(3)) for hx, hy, hz in product([-1, 1], repeat = 3) ]
			
	def __str__(self):
		return f'{self.id} - # points: {len(self.points)}'

	def __repr__(self):
		return self.__str__()

def parse_scanners(filename: str) -> List[Scanner]:
	with open(filename) as f:
		scanner_points = [ [ c for c in line.strip('\n').split('\n') ] for line in f.read().split('\n\n')]
	scanners = []
	for sp in scanner_points:
		points = [ Point(int(x), int(y), int(z)) for p in sp[1:] for x, y, z in [ p.split(',') ] ]
		scanners.append(Scanner(points))

	return scanners

def solve(scanners: List[Scanner]) -> int:
	# pull off the first scanner (0) and calculate the distances
	# from point to scanner (which we arbitrarily put at 0,0,0)
	cur_scanner = scanners.pop(0)
	processed_scanners = [ cur_scanner ]

	# for the rest of the scanners, identify the points in 
	# common and put them into the scanner's list of points
	while scanners:
		next_scanner = scanners.pop(0)

		# wow this is ugly!!!
		overlapping_points = None
		for s in processed_scanners:
			counts = defaultdict(list)
			for unknown_point in next_scanner.points:
				for rotated_point in next_scanner.point_rotations[unknown_point]:
					for known_point in s.points:
						diff = (known_point.x - rotated_point.x, known_point.y - rotated_point.y, known_point.z - rotated_point.z)
						counts[diff].append(next_scanner.point_rotations[unknown_point].index(rotated_point))

			overlapping_points = [ (k, v) for k, v in counts.items() if len(v) >= 12 ]
			if overlapping_points:
				offset = overlapping_points[0][0]
				rotations = overlapping_points[0][1]

				assert len(overlapping_points) == 1
				next_scanner.points = [ Point(offset[0] + p[rotations[0]].x, offset[1] + p[rotations[0]].y, offset[2] + p[rotations[0]].z) for p in next_scanner.point_rotations.values() ]
				next_scanner.center = Point(*offset)
				processed_scanners.append(next_scanner)
				break

		if len(overlapping_points) == 0:
			scanners.append(next_scanner)

	for s in processed_scanners:
		beacons = [ tuple((p.x, p.y, p.z)) for p in s.points ]
		Scanner.beacons |= set(beacons)

	print(len(Scanner.beacons))

	best = 0
	for s1, s2 in combinations(processed_scanners, 2):
		diff = abs(s1.center[0] - s2.center[0]) + abs(s1.center[1] - s2.center[1]) + abs(s1.center[2] - s2.center[2])
		if diff > best:
			best = diff
	print(best)

if __name__ == '__main__':
	scanners = parse_scanners('input.txt')
	solve(scanners)

