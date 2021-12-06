from aocd import lines
from collections import defaultdict
import re
from typing import List, Dict

test_lines = [
    '0,9 -> 5,9',
    '8,0 -> 0,8',
    '9,4 -> 3,4',
    '2,2 -> 2,1',
    '7,0 -> 7,4',
    '6,4 -> 2,0',
    '0,9 -> 2,9',
    '3,4 -> 1,4',
    '0,0 -> 8,8',
    '5,5 -> 8,2',
]

def parse_coords(lines : List, allow_diag = False) -> Dict:
    positions = defaultdict(int)
    rexp = re.compile("(\d+),(\d+) -> (\d+),(\d+)")
    for l in lines:
        m = rexp.fullmatch(l)
        assert(m is not None)
        x1, y1  = int(m.group(1)), int(m.group(2))
        x2, y2 = int(m.group(3)), int(m.group(4))
        dx = x2 - x1
        dy = y2 - y1
        xdir, ydir = 0, 0
        if dx != 0:
            xdir = int(dx / abs(dx))
        if dy != 0:
            ydir = int(dy / abs(dy) )
        if dx == 0 or dy == 0 or (allow_diag == True and (abs(x2 - x1) == abs(y2 - y1))):
            for i in range(max(abs(x2 - x1), abs(y2 - y1)) + 1):
                positions[ ( x1 + (xdir * i), y1 + (ydir * i) ) ] += 1

    return positions


if __name__ == '__main__': 
    # part1 - no diagonals
    positions = parse_coords(lines)
    overlap = sum( [ 1 for x in positions.values() if x > 1 ])
    print(overlap)

    # reparse, which is kind of dumb, but whatever
    positions = parse_coords(lines, True)
    overlap = sum( [ 1 for x in positions.values() if x > 1 ])
    print(overlap)
