# pylint: disable=missing-docstring, unused-import, mixed-indentation

import os
import sys
import collections
import queue
import threading
import time
import itertools

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from IntComputer import IntComputer

class Droid(IntComputer.IntComputer):
    def __init__(self, program, input_queue, output_queue):
        self._program = program
        self._computer = None
        self._id = id
        self.idle = False
        super().__init__( self._program, input_queue, output_queue )

    def _opinput(self, mode):
        # overrideen from base class to return -1
        # if there is no input to process
        if self.input_queue.empty() is True:
            command = input( )
            for c in command:
                self.input_queue.put(ord(c))
            self.input_queue.put(ord('\n'))

        c = self.input_queue.get()

        self._put_num(c, mode)

    def _opoutput(self, mode):
        value = self._get_num(mode)
        print (chr(value), end='')

commands = '''south
take space law space brochure
south
take mouse
south
take astrolabe
south
take mug
north
north
west
north
north
take wreath
south
south
east
east
north
west
north
take manifold
south
take sand
west
take monolith
west'''.split('\n')

items = 'monolith,wreath,mug,astrolabe,manifold,sand,mouse,space law space brochure'''.split(',')

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program =  [ int(x) for x in f.read().split(',') ]

    input_queue = queue.Queue( )
    output_queue = queue.Queue( )

    for cmd in commands:
        for c in cmd:
            input_queue.put(ord(c))
        input_queue.put(ord('\n'))

    droid = Droid(program, input_queue, output_queue)
    thread = threading.Thread( target = droid.run)
    thread.daemon = True     # allows thread to exit when main program exits
    thread.start( )


    # now try and figure out what combination of items we need to 
    have_items = items.copy( )
    dropped_items = [ ]
    for i in range(len(items)):
        for keep_items in itertools.combinations(items, i):
            drop_items = [ x for x in items if x not in keep_items ]

            for item in drop_items:
                cmd = 'drop ' + item + '\n'
                for c in cmd:
                    input_queue.put(ord(c))

            cmd = 'west' + '\n'
            for c in cmd:
                input_queue.put(ord(c))

            for item in drop_items:
                cmd = 'take ' + item + '\n'
                for c in cmd:
                    input_queue.put(ord(c))

    while True:
        pass
