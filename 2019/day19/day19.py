# pylint: disable=missing-docstring, unused-import, mixed-indentation

import os
import sys
import collections
import queue
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from IntComputer import IntComputer

class Drone():
    def __init__(self, program, show_display):
        self._program = program
        self._computer = None
        self._input_queue = queue.Queue()
        self._output_queue = queue.Queue()
        self._show_display = show_display

    def start(self, x, y):
        # start the int computer
        self._computer = IntComputer.IntComputer( self._program, self._input_queue, self._output_queue )
        self._input_queue.put(x)
        self._input_queue.put(y)
        thread = threading.Thread( target = self._computer.run)
        thread.start( )
        while self._computer.is_running == True:
            pass

        output = self._output_queue.get()
        return output
        

def run_program(x, y):
    drone = Drone( program, False )
    return drone.start(x, y)

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program =  [ int(x) for x in f.read().split(',') ]

    # part 1
    val = 0
    for x in range(50):
        for y in range(50):
            drone = Drone( program, False )
            val += drone.start(x, y)

    print(val)

    # part 2 - brute force, but simple
    x = 0
    y = 0
    while True:
        val = run_program(x + 99, y)
        if val == 1:
            break
        y = y + 1
        while True:
            val = run_program(x, y + 99)
            if val == 1:
                break
            x = x + 1
                
    print (x * 10000 + y)