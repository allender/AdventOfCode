# pylint: disable=missing-docstring, unused-import, mixed-indentation

import sys
import os
import enum
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from IntComputer import IntComputer
from collections import defaultdict

class Robot(IntComputer.IntComputer):

    class Direction(enum.Enum):
        UP = 0
        LEFT = 1
        DOWN = 2
        RIGHT = 3
        NUM_DIRS = 4

    def __init__(self, program):
        self.x = 0
        self.y = 0
        self.colors = defaultdict( int )
        self._painted = defaultdict( bool )
        self._direction = self.Direction.UP.value
        super().__init__(program)

    def move(self):
        if (self._direction == self.Direction.UP.value):
            self.x += 1
        elif (self._direction == self.Direction.LEFT.value):
            self.y -= 1
        elif (self._direction == self.Direction.DOWN.value):
            self.x -= 1
        elif (self._direction == self.Direction.RIGHT.value):
            self.y += 1

    def turn_left_and_move(self):
        self._direction = (self._direction + 1) % self.Direction.NUM_DIRS.value
        self.move( )

    def turn_right_and_move(self):
        self._direction = (self._direction - 1) % self.Direction.NUM_DIRS.value
        self.move( )

    def get_color(self):
        color = self.colors[ (self.x, self.y) ]
        return color

    def set_color(self, color):
        self.colors[ (self.x, self.y ) ] = color
        self._painted[ (self.x, self.y ) ] = True

    def get_num_painted(self):
        return len( [ x for x in self._painted.values() if x is True ] )

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program = f.read()

    robot = Robot(program)
    robot.inputs = [ 0 ]

    while( True ):
        robot.run()
        if (robot.is_running is False):
            break

        # get the color and then move the robot
        color = robot.outputs.pop(0)
        robot.set_color( color )
        dir = robot.outputs.pop(0)
        assert( dir == 0 or dir == 1 )
        if dir ==  0:
            robot.turn_left_and_move( )
        elif dir == 1:
            robot.turn_right_and_move( )

        robot.inputs.append( robot.get_color( ) )

    print (robot.get_num_painted( ) )

    # part 2
    robot = Robot(program)
    robot.inputs = [ 1 ]

    while( True ):
        robot.run()
        if (robot.is_running is False):
            break

        # get the color and then move the robot
        color = robot.outputs.pop(0)
        robot.set_color( color )
        dir = robot.outputs.pop(0)
        assert( dir == 0 or dir == 1 )
        if dir ==  0:
            robot.turn_left_and_move( )
        elif dir == 1:
            robot.turn_right_and_move( )

        robot.inputs.append( robot.get_color( ) )

    minx, miny, maxx, maxy = 0, 0, 0, 0
    for ( x, y ) in robot.colors.keys( ):
        minx = min(minx, x)
        miny = min(miny, y)
        maxx = max(maxx, x)
        maxy = max(maxy, y)

    for x in range(maxx, minx - 1, -1):
        for y in range(miny, maxy + 1):
            if (x, y) in robot.colors:
                val = robot.colors[ (x, y) ]
            else:
                val = 0

            if val == 0:
                print (' ', end = '')
            else:
                print ('.', end = '')

        print( '' )

    print( '' )
