# pylint: disable=missing-docstring, unused-import, mixed-indentation

import os
import sys
import collections
import queue
import threading
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from IntComputer import IntComputer

class NIC(IntComputer.IntComputer):
    def __init__(self, program, id, input_queue, output_queue):
        self._program = program
        self._computer = None
        self._id = id
        self.idle = False
        super().__init__( self._program, input_queue, output_queue )

    def _opinput(self, mode):
        # overrideen from base class to return -1
        # if there is no input to process
        try:
            input = self.input_queue.get( block = False)
            self.idle = False
        except queue.Empty:
            input = -1
            self.idle = True

        self._put_num(input, mode)

class Network():
    def __init__(self, count, program):
        self.num_nics = count
        self.nodes = [ ]
        self.input_queues = [ ]
        self.output_queues = [ ]
        self.nat_queue = queue.Queue()
        self.nat_last_y = None

        for i in range( self.num_nics ):
            self.input_queues.append( queue.Queue( ) )
            self.input_queues[-1].put( i )
            self.output_queues.append( queue.Queue( ) )
            self.nodes.append( NIC(program, i, self.input_queues[-1], self.output_queues[-1]) )

    def check_output_queues( self ):
        for q in self.output_queues:
            node = None
            if q.qsize() >= 3:
                node = q.get( )
                x = q.get( )
                y = q.get( )

                if node == 255:
                    # create a new queue which has the effect of remembering the last
                    # x/y pair that was sent.
                    print('{0} sending {1},{2} to {3}'. format(self.output_queues.index(q), x, y, node))
                    self.nat_queue = queue.Queue( )
                    self.nat_queue.put( x )
                    self.nat_queue.put( y )

                elif node is not None and 0 <= node <= self.num_nics:
                    self.input_queues[node].put( x )
                    self.input_queues[node].put( y )

    def check_nat(self):
        idle = all(i.idle == True for i in self.nodes)
        if idle is True and self.nat_queue.empty() is False:
            x = self.nat_queue.get( )
            y = self.nat_queue.get( )

            self.input_queues[0].put( x )
            self.input_queues[0].put( y )
            
            if self.nat_last_y == y:
                print('twice in a row: {0}, {1}'.format(self.nat_last_y, y))
                sys.exit(0)

            self.nat_last_y = y


    def monitor(self):
        while True:
            # step all of the nics.  GIL kills us in python so we will just
            # run all of the nodes iteratively.  NIC overrides the input function
            # to keep track of idle.
            for nic in self.nodes:
                nic.step( )

            # check output queues to see if we need to forward packs
            # to another nic or the nat
            self.check_output_queues( )

            # see if we have data for the NAT
            self.check_nat( )


if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program =  [ int(x) for x in f.read().split(',') ]

    network = Network(50, program)
    network.monitor( )
