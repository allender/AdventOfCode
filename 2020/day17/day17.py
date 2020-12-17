
test_data = """.#.
..#
###"""

if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')

    cubes_on = set()
    for row, line in enumerate(data):
        for col, ch in enumerate(line):
            if ch == '#':
                cubes_on.add((row, col, 0))


    v = [-1, 0, 1]
    dirs = [ (x, y, z) for x in v for y in v for z in v ]
    coords_to_check = [ (x, y, z) for x in range(-15, 15) for y in range(-15,15) for z in range(-8, 8) ]
    for _ in range(6):
        new_cubes = set()
        for (x, y, z) in coords_to_check:
            neighbors_on = 0
            for d in dirs:
                if d[0] != 0 or d[1] != 0 or d[2] != 0:
                    if (x + d[0], y + d[1], z + d[2]) in cubes_on:
                        neighbors_on += 1

            if (x, y, z) not in cubes_on and neighbors_on == 3:
                new_cubes.add((x, y, z))
            elif (x, y, z) in cubes_on and 2 <= neighbors_on <= 3:
                new_cubes.add((x, y, z))

        cubes_on = new_cubes

    print(len(cubes_on))

    cubes_on = set()
    for row, line in enumerate(data):
        for col, ch in enumerate(line):
            if ch == '#':
                cubes_on.add((row, col, 0, 0))

    dirs = [ (x, y, z, w) for x in v for y in v for z in v for w in v]
    coords_to_check = [ (x, y, z, w) for x in range(-15, 15) for y in range(-15, 15) for z in range(-8, 8) for w in range(-8, 8) ]
    for _ in range(6):
        new_cubes = set()
        for (x, y, z, w) in coords_to_check:
            neighbors_on = 0
            for d in dirs:
                if d[0] != 0 or d[1] != 0 or d[2] != 0 or d[3] != 0:
                    if (x + d[0], y + d[1], z + d[2], w + d[3]) in cubes_on:
                        neighbors_on += 1

            if (x, y, z, w) not in cubes_on and neighbors_on == 3:
                new_cubes.add((x, y, z, w))
            elif (x, y, z, w) in cubes_on and 2 <= neighbors_on <= 3:
                new_cubes.add((x, y, z, w))

        cubes_on = new_cubes

    print(len(cubes_on))

