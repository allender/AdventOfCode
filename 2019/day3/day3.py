import collections
import sys

def get_points(wire_directions):
    positions = set()
    x, y = 0, 0
    for direction in wire_directions:
        d = direction[0]
        num = int(direction[1:])
        for _ in range(num):
            if (d == 'R'):
                x += 1
            elif (d == 'U'):
                y += 1
            elif (d == 'L'):
                x -= 1
            elif (d == 'D'):
                y -= 1

            positions.add( (x, y) )

    return positions

def get_distance(wire_directions, crossings):
    crossing_distance = { }
    x, y, distance = 0, 0, 0
    for direction in wire_directions:
        d = direction[0]
        num = int(direction[1:])
        for _ in range(num):
            if (d == 'R'):
                x += 1
            elif (d == 'U'):
                y += 1
            elif (d == 'L'):
                x -= 1
            elif (d == 'D'):
                y -= 1

            distance += 1

            if ((x,y) in crossings):
                crossing_distance[(x,y)] = distance

    return crossing_distance


def manhattan(pos):
    return abs(pos[0]) + abs(pos[1])

if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()

    # each line represents a wire, so "compile" the
    # wire into coordinates
    wire_positions = [ ]
    for line in lines:
        wire_directions = line.strip().split(',')
        wire_positions.append(get_points(wire_directions))

    # after getting wire positions, find the intersections
    intersections = wire_positions[0].intersection(wire_positions[1])

    # part 1
    #result = min(manhattan(pos) for pos in intersections)

    # find the minimal distance to each crossing
    crossing_distances = []
    for line in lines:
        wire_directions = line.strip().split(',')
        crossing_distances.append(get_distance(wire_directions, intersections))

    min_distance = min(crossing_distances[0][crossing] + crossing_distances[1][crossing] for crossing in intersections)
    print (min_distance)