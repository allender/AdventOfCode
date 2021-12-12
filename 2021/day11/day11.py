from aocd import lines
from typing import List, Tuple
from collections import defaultdict

test_lines = [
    '5483143223',
    '2745854711',
    '5264556173',
    '6141336146',
    '6357385478',
    '4167524645',
    '2176841721',
    '6882881134',
    '4846848554',
    '5283751526',
]

small_test_lines = [
    '11111',
    '19991',
    '19191',
    '19991',
    '11111',
]

def parse_lines(lines : List[str]) -> dict:
    # create an int dict and then "surround" the points
    # the 9's which will prevent flood filling ouf of the
    # grid
    points = defaultdict(int)
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            points[(x, y)] = int(lines[y][x])

    return points

dirs = [ (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1) ]

def step(point: tuple, points: dict) -> int:
    if point not in points:
        return

    points[ point ] += 1
    if points[ point ] == 10:
        for dir in dirs:
            step( (point[0] + dir[0], point[1] + dir[1]), points)

def do_sim(points: dict) -> Tuple[ int, int ]:
    num_steps = 0
    total_at_100 = 0
    while True:
        for point in points:
            step(point,  points)

        num_flashes = sum( [1 for x in points.values() if x >= 10])
        num_steps += 1

        # count number of flashes for the first 100 steps
        if num_steps < 100:
            total_at_100 += num_flashes

        # 100 means that all of the octopi flashed so
        # we can bail
        if (num_flashes == 100):
            break
        
        for x in points:
            if points[x] >= 10:
                points[x] = 0

    return total_at_100, num_steps

if __name__ == '__main__': 
    points = parse_lines(lines)
    total_at_100, step_at_full = do_sim(points)
    print(total_at_100, step_at_full)
