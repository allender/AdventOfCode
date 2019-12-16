# pylint: disable=missing-docstring, unused-import, mixed-indentation
import sys
import os
import time
import queue
import threading
from collections import deque
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from IntComputer import IntComputer

class Robot():

    def __init__(self, program, show_display):
        self._program = program
        self._computer = None
        self.oxygen_pos = None
        self.pos = ( 0, 0 )
        self.free = set( )
        self._input_queue = queue.Queue()
        self._output_queue = queue.Queue()

    def print_display(self):
        pass

    def neighbors(self, x, y):
        return [((x, y - 1), 1), ((x, y + 1), 2), ((x - 1, y), 3), ((x + 1, y), 4)]

    def path(self, src, dst, free):
        if src == dst:
            return []
        visited = set()
        queue = deque(((src, []), ))
        while True:
            pos, path = queue.popleft()
            for next_pos, direction in self.neighbors(*pos):
                if next_pos == dst:
                    # return path + [(pos2, direction)]
                    path.append( (next_pos, direction) )
                    return path
                if next_pos in visited or next_pos not in free:
                    continue
                queue.append((next_pos, path + [(next_pos, direction)]))
                visited.add(next_pos)
            
    def start(self):
        # start the int computer
        self._computer = IntComputer.IntComputer( self._program, self._input_queue, self._output_queue )
        thread = threading.Thread( target = self._computer.run)
        thread.daemon = True     # allows thread to exit when main program exits
        thread.start( )

        positions = { (0, 0) }
        visited = set( )

        while positions:
            target, value = positions.pop(), 1
            visited.add(target)
            for next_pos, direction in self.path(self.pos, target, self.free):
                self._input_queue.put(direction)
                value = self._output_queue.get()
                if value == 0:
                    break
                self.pos = next_pos
                if value == 2:
                    self.oxygen_pos = self.pos
            if value:
                self.free.add(self.pos)

            positions.update(next_pos for next_pos, _ in self.neighbors(*self.pos) if next_pos not in visited)

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program =  [ int(x) for x in f.read().split(',') ]

    # part 1
    robot = Robot( program, False )
    robot.start( )
    #robot.print_display()
    print ( len(robot.path((0,0), robot.oxygen_pos, robot.free)) )

    # part 2
    print (max(len(robot.path(robot.oxygen_pos, pos, robot.free)) for pos in robot.free))
