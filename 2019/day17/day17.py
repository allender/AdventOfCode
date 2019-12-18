# pylint: disable=missing-docstring, unused-import, mixed-indentation

import os
import sys
import collections
import queue
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from IntComputer import IntComputer

Point = collections.namedtuple('Point', ['x', 'y'])

class Robot():
    def __init__(self, program, show_display):
        self._program = program
        self._computer = None
        self.tiles = { } 
        self.min_pos = Point( -1, -1 )
        self.max_pos = Point( -1, -1 )
        self.start_pos = Point( -1, -1 )
        self._input_queue = queue.Queue()
        self._output_queue = queue.Queue()
        self._show_display = show_display

    def start(self, input_data = None):
        # start the int computer
        self._computer = IntComputer.IntComputer( self._program, self._input_queue, self._output_queue )
        thread = threading.Thread( target = self._computer.run)
        thread.daemon = True     # allows thread to exit when main program exits
        thread.start( )

        # if we have input, stick it on the input queue
        if input_data is not None:
            for i in input_data:
                self._input_queue.put( ord(i) )

        x, y = 0, 0
        num_output = ''
        while self._computer.is_running is True:
            pass
        
        while self._output_queue.empty() is False:
            output = self._output_queue.get( )

            # when there is no input data, we should get putting together
            # the grid for the robot
            if input_data is None:
                output = chr( output )
                if output in ['\n', '#', '.', '^', '<', '>', 'v', 'X']:
                    if output == '\n':
                        y += 1
                        x = 0
                    else:
                        # see if this is the start of the robot
                        # and then save it so that we can then use it
                        # as starting pos for finding crossings
                        if output == '^':
                            self.start_pos = Point(x, y)
                        self.tiles[Point(x, y)] = output
                        x += 1
                else:
                    print(output)
            else:
                if output < 255:
                    print(chr(output), end='')
                else:
                    print(output)

        if self._show_display:
            print( '{:c}[2J'.format( 27 ) )
            for point, char in self.tiles.items():
                print('{:c}[{};{}f{}'.format( 27, point.y+1, point.x+1, char ))
                

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program =  [ int(x) for x in f.read().split(',') ]

    # part 1
    robot = Robot( program, False )
    robot.start( )

    # part 1
    # find all intersections
    alignment = 0
    for point in robot.tiles.keys():
        try:
            if robot.tiles[point] == '#' and \
              robot.tiles[(point.x-1, point.y)] == '#' and \
              robot.tiles[(point.x+1, point.y)] == '#' and \
              robot.tiles[(point.x, point.y-1)] == '#' and \
              robot.tiles[(point.x, point.y+1)] == '#':
                alignment += (point.x * point.y)
        except KeyError:
            continue

    print(alignment)

    # part 2 - do it programmatically
    pos = robot.start_pos
    commands = [ ]

    # used to help determine which way to move next
    dirs = [ Point(-1, 0), Point(0, -1), Point(1, 0), Point(0, 1) ]

    # start pointing up
    dir_index = 1
    count = 0
    command = ''
    while True:
        while True:
            new_pos = Point(pos.x + dirs[dir_index].x, pos.y + dirs[dir_index].y)
            if new_pos in robot.tiles and robot.tiles[new_pos] == '#':
                pos = new_pos
                count += 1
            else:
                break

        if count > 0:
            commands.append( (command, count) )
            count = 0

        # determine which way to move and the direction
        new_pos = [ Point(pos.x + d.x, pos.y + d.y) for d in dirs ]
        new_index = -1
        for num, p in enumerate(new_pos):
            if p not in robot.tiles or dir_index == num or dir_index == ((num + 2) % 4):
                continue
            if (robot.tiles[p] == '#'):
                if ((num+1) % 4) == dir_index:
                    command = 'L'
                else:
                    command = 'R'
                new_index = num
                break

        # we have reached the end of the line for the robot
        if new_index == -1:
            break

        dir_index = new_index

    # still working on trying to detemine how to find programs programmatically
    # but hard examinined for now
    full_program = 'A,B,A,B,C,C,B,A,B,C\n'
    for command in commands[0:4]:
        full_program += command[0] + ',' + str(command[1]) + ','
    full_program = full_program[:-1] + '\n'

    for command in commands[4:7]:
        full_program += command[0] + ',' + str(command[1]) + ','
    full_program = full_program[:-1] + '\n'

    for command in commands[14:17]:
        full_program += command[0] + ',' + str(command[1]) + ','
    full_program = full_program[:-1] + '\n'

    full_program += 'n\n'

    program[0] = 2
    robot = Robot( program, False )
    robot.start( full_program )
    # determine the three programs to run
    # programs = [ ]
    # cur_index = 0
    # next_command = None
    # prog = [ ]
    # while True:
    #     command = commands.pop(0)
    #     prog.append(command)
    #     if next_command is None:
    #         next_command = commands.index(command)
    #     else:
    #         next_command -= 1

    #     if next_command < 0 or command != commands[next_command]:
    #         programs.append( prog )
    #         prog = [ command ]
    #         next_command = commands.index(command)

    #     commands.pop(next_command)

    # print (commands)
    


        
