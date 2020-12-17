import sys
import itertools
import operator

test_data = """.#.
..#
###"""

def solve(active_cubes, num_dim, num_iterations):
    v = [-1, 0, 1]
    zero = ( 0, ) * num_dim
    for _ in range(6):
        # find actual neighbors to check
        neighbors = set()
        for c in active_cubes:
            neighbors = neighbors.union( [ tuple(map(sum, zip(c, d))) for d in itertools.product([-1, 0, 1], repeat = num_dim) if d != zero] )

        new_active_cubes = set()
        for cell in neighbors:
            cell_neighbors = set( [ tuple(map(sum, zip(cell, d))) for d in itertools.product([-1, 0, 1], repeat = num_dim) if d != zero] )
            if cell in active_cubes and len(active_cubes.intersection(cell_neighbors)) in (2, 3):
                new_active_cubes.add(cell)
            elif cell not in active_cubes and len(active_cubes.intersection(cell_neighbors)) == 3:
                new_active_cubes.add(cell)

        active_cubes = new_active_cubes

    print(len(active_cubes))
    

if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')

    active_cubes = set()
    for row, line in enumerate(data):
        for col, ch in enumerate(line):
            if ch == '#':
                active_cubes.add((row, col, 0))

    solve(active_cubes, 3, 6)

    active_cubes = set()
    for row, line in enumerate(data):
        for col, ch in enumerate(line):
            if ch == '#':
                active_cubes.add((row, col, 0, 0))

    solve(active_cubes, 4, 6)
