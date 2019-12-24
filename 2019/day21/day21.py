# pylint: disable=missing-docstring, unused-import, mixed-indentation

import os
import sys
import collections
import queue
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from IntComputer import IntComputer

class SpringDroid():
    def __init__(self, program, show_display):
        self._program = program
        self._computer = None
        self._input_queue = queue.Queue()
        self._output_queue = queue.Queue()
        self._show_display = show_display

    def start(self, script):
        # start the int computer
        self._computer = IntComputer.IntComputer( self._program, self._input_queue, self._output_queue )

        thread = threading.Thread( target = self._computer.run)
        thread.daemon = True     # allows thread to exit when main program exits
        thread.start( )
        
        # convert the list of commands to a list of ascii codes
        input_values = list(map(ord, list('\n'.join(script) + '\n')))
        for val in input_values:
            self._input_queue.put(val)

        while self._computer.is_running == True:
            pass

        while True:
            try:
                output = self._output_queue.get_nowait()
                if output > 128:
                    return output
                print("{:c}".format(output), end='')
            except queue.Empty:
                return 0
        

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program =  [ int(x) for x in f.read().split(',') ]

    spring_droid = SpringDroid(program, False)
    script = [
        'NOT A T',
        'NOT B J',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'WALK']
    output = spring_droid.start(script)
    print(output)


    spring_droid = SpringDroid(program, False)
    script = [
        'NOT A T',
        'NOT B J',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'AND D J',
        'NOT E T',
        'NOT T T',
        'OR H T',
        'AND T J',
        'RUN']
    output = spring_droid.start(script)
    print(output)
