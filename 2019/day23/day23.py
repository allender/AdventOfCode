# pylint: disable=missing-docstring, unused-import, mixed-indentation

import os
import sys
import collections
import queue
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from IntComputer import IntComputer

class NIC():

    # list of all NICs
    nodes = [ ]
    _lock = threading.Lock()

    def __init__(self, program, ident):
        self._program = program
        self._computer = None
        self._id = ident
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self._output_count = 0
        self.input_queue.put( self._id )
        NIC.nodes.append(self)

    def start(self):
        self._computer = IntComputer.IntComputer( self._program, self.get_input, self.send_output )
        thread = threading.Thread( target = self._computer.run)
        thread.daemon = True     # allows thread to exit when main program exits
        thread.start( )

    def get_input(self):
        value = -1
        if self.input_queue.empty() is False:
            value = self.input_queue.get( )

        # print("{0} getting {1}".format(self._id, value))

        return value

    def send_output(self, value):
        # print('{0} needs to output'. format(self._id))
        self.output_queue.put(value)
        self._output_count += 1
        if self._output_count == 3:
            node = self.output_queue.get( )
            x = self.output_queue.get( )
            y = self.output_queue.get( )

            if node == 255:
                print ('{0} sends x/y  {1}/{2}'.format(node, x, y))
            else:
                NIC.nodes[node].input_queue.put( x )
                NIC.nodes[node].input_queue.put( y )
                self._output_count = 0

    def send( self, x, y ):
        self._input_queue.put( x )
        self._input_queue.put( y )

    @staticmethod
    def start_all( ):
        for node in NIC.nodes:
            node.start( )


if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program =  [ int(x) for x in f.read().split(',') ]

    num_nics = 50 
    for i in range(num_nics):
        nic = NIC(program, i)

    NIC.start_all( )

    while True:
        pass