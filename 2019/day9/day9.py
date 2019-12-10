# pylint: disable=missing-docstring, unused-import, mixed-indentation

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from IntComputer import IntComputer

class Boost(IntComputer.IntComputer):
    pass

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program = f.read()

    boost = Boost(program)
    boost.inputs = [ 1 ]
    boost.run()
    print (boost.output)

    boost.reset()
    boost.inputs = [ 2 ]
    boost.run( )
    print (boost.output)
