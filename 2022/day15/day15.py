from aocd.models import Puzzle
import re

puzzle = Puzzle(year=2022, day = 15)

test_data = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''

class Point2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.x}, {self.y}'

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, rhs):
        return self.x == rhs.x and self.y == rhs.y

    def manhattan_dist(self, p):
        return abs(self.x - p.x) + abs(self.y - p.y)

class Grid():
    def __init__(self, sensors, beacons):
        self.cells = {}
        self.distances = {}
        all_points = [ x for x in sensors + beacons ]
        self.min = Point2(min( [ x.x for x in all_points ] ), min( [ x.y for x in all_points ] ))
        self.max = Point2(max( [ x.x for x in all_points ] ), max( [ x.y for x in all_points ] ))
        self.pairs = list(zip(sensors, beacons))
        for s, b in self.pairs:
            self.cells[(s.x, s.y)] = 'S'
            self.cells[(b.x, b.y)] = 'B'

            self.distances[(s,b)] = s.manhattan_dist(b)

    def solve_part1(self, row: int):
        ranges = []
        for sensor, beacon in self.pairs:

            # find distance along y axis from this sensor to the row to 
            # see if we should even look at it
            dist_to_row = abs(sensor.y - row)
            if dist_to_row > self.distances[(sensor,beacon)]:
                continue

            diff = self.distances[(sensor, beacon)] - dist_to_row
            startx = sensor.x - diff
            endx = sensor.x + diff + 1
            ranges.append((startx, endx))

        # determine the number of becons on the given row because we don't wnat
        # to count those
        count = len( {b.x for _,b in self.pairs if b.y == row})
        start, end = zip(*ranges)
        return max(end) - min(start) - count

    def solve_part2(self, limit):
        for row in range(limit):
            ranges = []
            for sensor, beacon in self.pairs:

                # find distance along y axis from this sensor to the row to 
                # see if we should even look at it
                dist_to_row = abs(sensor.y - row)
                if dist_to_row > self.distances[(sensor,beacon)]:
                    continue

                diff = self.distances[(sensor, beacon)] - dist_to_row
                startx = sensor.x - diff
                endx = sensor.x + diff + 1
                ranges.append((startx, endx))

            ranges = sorted(ranges, key = lambda x: x[0])

            # with the sorted ranges, there should be no gaps.  A gap is the
            # beacon
            last_column = 0
            iter = 0
            for iter in range(len(ranges) - 1):
                (min1, max1), (min2, max2) = ranges[iter], ranges[iter + 1]
                if min2 > last_column and min2 > max1:
                    return max1 * 4000000 + row
                last_column = max(max1, last_column)

def parse_input(data):
    sensors = []
    beacons = []
    for l in data.splitlines():
        x_points = [ int(x.split('=')[1]) for x in re.findall(r'x=[-]*\d+', l) ]
        y_points = [ int(y.split('=')[1]) for y in re.findall(r'y=[-]*\d+', l) ]
        sensor, beacon = zip(x_points, y_points)
        sensors.append(Point2(*sensor))
        beacons.append(Point2(*beacon))

    return Grid(sensors, beacons)

data = puzzle.input_data
row_to_check = 2000000
limit = 4000000
# data = test_data
# row_to_check = 10
# limit = 20
grid = parse_input(data)
print(grid.solve_part1(row_to_check))
print(grid.solve_part2(limit))