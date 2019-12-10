# pylint: disable=missing-docstring, unused-import, mixed-indentation

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from IntComputer import IntComputer

def run_program(opcodes):
    ip = 0
    while (True):
        opcode = opcodes[ip]
        num1 = opcodes[opcodes[ip + 1]]
        num2 = opcodes[opcodes[ip + 2]]
        dest = opcodes[ip + 3]
        if (opcode == 1):
            num3 = num1 + num2
        elif (opcode == 2):
            num3 = num1 *  num2
        elif (opcode == 99):
            break
        else:
            assert("bad juju")
        
        opcodes[dest] = num3
        ip += 4



if __name__ == '__main__':
    with open('input.txt') as f:
        program = f.read()

    machine = IntComputer.IntComputer( program )
    machine.memory.set( 1, 12 )
    machine.run( )
    print ( machine.memory.get(0) )

    ip = 0
    values = range(0, 99)
    for x in values:
        for y in values: 
            machine = IntComputer.IntComputer( program )
            machine.memory.set( 1, x )
            machine.memory.set( 2, y )
            machine.run( )
            if ( machine.memory.get( 0 ) == 19690720 ):
                print (100 * machine.memory.get( 1 ) + machine.memory.get( 2 ) )
                sys.exit(0)
