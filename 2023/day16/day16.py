from aocd.models import Puzzle
from collections import defaultdict

puzzle = Puzzle(2023, 16)

inputs = puzzle.input_data.strip().split('\n')
# inputs = puzzle.examples[0][0].split('\n')

map = { complex(x, y): c for y,l in enumerate(inputs) for x,c in enumerate(l) }

dirs = {
    '|': { 1 : (-1j, 1j),
          -1 : (-1j, 1j) },

    '-': { -1j : (1, -1),
            1j : (1, -1) },

    '/': { 1 : (-1j, ),
          -1 : (1j, ),
          -1j : (1, ),
           1j : (-1, ) },

    '\\': { 1 : (1j, ),
           -1 : (-1j, ),
           -1j : (-1, ),
           1j : (1, ), }
}

def follow_path(points):
    visited = defaultdict(int)
    seen_splitters = []
    while points:
        point,dir = points.pop(0)
        if point.real < 0 or point.real >= len(inputs[0]):
            continue
        elif point.imag < 0 or point.imag >= len(inputs):
            continue

        if map[point] in ['-', '|'] and point in seen_splitters:
            continue

        # keep track of where we have been
        visited[point] += 1

        # fiogure out where to go from here
        if map[point] in dirs and dir in dirs[map[point]]:
            if map[point] in ['-', '|']:
                seen_splitters.append(point)

            points.extend([ (point + new_d, new_d) for new_d in dirs[map[point]][dir] ])
        else:
            points.insert(0, (point + dir, dir))

    return visited


start = [ (complex(0.0), complex(1,0)) ]
visited = follow_path(start)
print(len(visited))

lengths = []
for x in range(len(inputs[0])):
    start = [ (complex(x, 0), complex(0, 1)) ]
    lengths.append(len(follow_path(start)))

    start = [ (complex(x, len(inputs) - 1), complex(0, -1)) ]
    lengths.append(len(follow_path(start)))

for y in range(len(inputs)):
    start = [ (complex(0, y), complex(1, 0)) ]
    lengths.append(len(follow_path(start)))

    start = [ (complex(len(inputs[0]) - 1, y), complex(-1, 0)) ]
    lengths.append(len(follow_path(start)))

print(max(lengths))
