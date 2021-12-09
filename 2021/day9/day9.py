from aocd import lines
from typing import List
from collections import defaultdict
from functools import reduce
from operator import mul

test_lines = [
    '2199943210',
    '3987894921',
    '9856789892',
    '8767896789',
    '9899965678',
]

# directions for adjacent points
adjacent = [ (-1, 0), (0, -1), (1, 0), (0, 1) ]
def is_low(point, points):
    x = point[0]
    y = point[1]
    for a in adjacent:
        x1 = x + a[0]
        y1 = y + a[1]
        if ((x1,y1) in points and points[(x1,y1)] <= points[point]):
            return False
        
    return True

def part1(points):
    # iteraste through all keys in the dict and then we can calculate
    # is that point is a minimum
    risk_level = 0
    low_points = []
    for point in points.keys():
        if is_low(point, points):
            low_points.append(point)
            risk_level += points[point] + 1

    return low_points, risk_level

def find_basin(basin_point_list : List, basin_points, points):
    if not basin_point_list:
        return 0


    return 0 

def part2(points, low_points):
    # find all of the addjacent points to this low point
    basin_sizes = []
    for low_point in low_points:
        points_to_check = [low_point]
        basin_points = []
        while points_to_check:
            point = points_to_check.pop(0)
            if point not in basin_points:
                basin_points.append(point)
            x = point[0]
            y = point[1]
            for a in adjacent:
                x1 = x + a[0]
                y1 = y + a[1]
                if ((x1,y1) in points and (x1, y1) not in basin_points and points[(x1,y1)] < 9):
                    points_to_check.append((x1, y1))
        
        basin_sizes.append(len(basin_points))

    basin_sizes.sort()
    return reduce(mul, basin_sizes[-3:], 1)



if __name__ == '__main__': 
    points = defaultdict(int) 
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            points[(x, y)] = int(lines[y][x])

    low_points, risk_level = part1(points)
    print(risk_level)
    print(part2(points, low_points))