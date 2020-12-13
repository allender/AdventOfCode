import sys
import math

sys.path.append('../..')

import utils

test_data = """F10
N3
F7
R90
F11"""

fvecs = [ (1, 0), (0, -1), (-1, 0), (0, 1) ]
values = 'ESWNLRF'

if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')
    current_direction = 0
    ship = [0, 0]
    for d in data:
        index, length = values.index(d[0]),int(d[1:])
        if index < 4:
            ship = [ x + (fvecs[index][i]) * length for i,x in enumerate(ship) ]
        elif 4 <= index <= 5:
            degrees = length / 90
            current_direction = int((current_direction - (degrees * ((-1)**index))) % 4)
        else:
            ship = [ x + fvecs[current_direction][i] * length for i, x in enumerate(ship) ]
    
    print(abs(ship[0]) + abs(ship[1]))

    ship = [0, 0]
    waypoint = [10, 1]
    for d in data:
        index, length = values.index(d[0]),int(d[1:])
        if index < 4:
            waypoint = [ x + (fvecs[index][i]) * length for i,x in enumerate(waypoint) ]
        elif 4 <= index <= 5:
            theta = math.radians(length) * ((-1)**index)
            waypoint = [ int(round(waypoint[0] * math.cos(theta) - waypoint[1] * math.sin(theta), 0)), int(round(waypoint[0] * math.sin(theta) + waypoint[1] * math.cos(theta), 0)) ]
        else:
            ship = [ x + waypoint[i] * length for i, x in enumerate(ship) ]
    
    print(abs(ship[0]) + abs(ship[1]))
