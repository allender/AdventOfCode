# pylint: disable=missing-docstring, unused-import, mixed-indentation
import sys
import math
from collections import namedtuple, defaultdict
from itertools import cycle

Point = namedtuple('Point', [ 'x', 'y' ] )

def get_angle( point1, point2 ):
    angle = math.degrees(math.atan2(point1.x - point2.x, point1.y - point2.y) % (2 * math.pi ) )
    return  angle

def visible( asteroids, a ):
    return len(set(get_angle(a, b) for b in asteroids if a != b))

def part1( asteroids ):
    return max(visible(asteroids, a) for a in asteroids)

def part2( asteroids ):
    base = max(asteroids, key=lambda a: visible(asteroids, a))
    asteroids.remove( base )
    angles = defaultdict(list)

    # get the angles to all of the other asteroids from the base.  Weird
    # case of having to deal with 360/0 being the same.  I don't lik this
    # but getting it working first
    for a in asteroids:
        ang = 360 - get_angle( base, a )
        if ang == 360.0:
            ang = 0.0
        angles[ang].append(a)

    # sort the asteroids closest to farthest from the base.  Don't
    # need exact distance - just need to know what is further away
    sorted_asteroids = [ angles[angle] for angle in sorted(angles.keys()) ]
    for a in sorted_asteroids:
        a.sort(key=lambda a: ((base.x - a.x) ** 2) + ((base.y - a.y) ** 2))

    # kind of cheat and use cycle iterator and then just break
    # when we need to
    destroyed_asteroids = [ ]
    for num, point in enumerate(cycle(sorted_asteroids)):
        if point:
            destroyed_asteroids.append( point.pop(0) )
        if num == 199:
            break
            
    return destroyed_asteroids[199].x * 100 + destroyed_asteroids[199].y

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        lines = f.read( ).splitlines( )

    asteroids = [ Point(x, y) for y, l in enumerate(lines) for x, loc in enumerate(l) if loc == '#' ]

    #print( part1( asteroids ) )
    print( part2( asteroids ) )