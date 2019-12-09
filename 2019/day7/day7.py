# pylint: disable=missing-docstring, unused-import, mixed-indentation
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from IntComputer import IntComputer
from itertools import permutations

class Amplifier(IntComputer.IntComputer):

    def __init__(self, program):
        self.phase = -1
        self._program = program
        super().__init__(program)

    def add_input(self, input):
        self.inputs.append( input )


# create list of all possible phase inputs.  Can't duplicate
# phase settings so we go with ugly if statements for now
def get_initial_phases(start, end):
    return list( permutations( range(start, end) ) )

def run_part1(amplifiers):
    phase_inputs = get_initial_phases( 0, 5 )
    max_output = 0

    # iterate through all possible phase inputs
    for phase_input in phase_inputs:
        # set inputs for all amplifiers
        for num, amp in enumerate(amplifiers):
            amp.reset( )
            amp.add_input(phase_input[num])

        current_output = 0
        for amp in amplifiers:
            amp.add_input( current_output )
            amp.run( )
            current_output = amp.output

        max_output = max(current_output, max_output)

    print (max_output)

def run_part2( amplifiers ):
    phase_inputs = get_initial_phases( 5, 10 )
    max_output = 0

    # iterate through all possible phase inputs
    for phase_input in phase_inputs:

        # preload the phase input for all amps
        for num, amp in enumerate(amplifiers):
            amp.reset( )
            amp.add_input(phase_input[num])

        current_output = 0
        while (True):
            for amp in amplifiers:
                amp.add_input( current_output )
                amp.run( )
                current_output = amp.output

            max_output = max(current_output, max_output)

            if amplifiers[4].is_running == False:
                break


    print (max_output)


if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program = f.read()

    amplifiers = [ ]
    for amp in range(0,5):
        amplifiers.append(Amplifier(program))

    run_part1( amplifiers )
    run_part2( amplifiers )
