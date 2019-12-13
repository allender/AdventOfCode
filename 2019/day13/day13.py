# pylint: disable=missing-docstring, unused-import, mixed-indentation
import sys
import os
import time
import queue
import threading
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from IntComputer import IntComputer

class Arcade():

    def __init__(self, program, show_display):
        self._program = program
        self.tiles = { }
        self.score = 0
        self.show_display = show_display
        self._input_queue = queue.Queue()
        self._output_queue = queue.Queue()

    def _print_display(self, x, y):
        if self.show_display == False:
            return

        # use ansi color to print out the board.  Use the background
        # colors in order from 40 (black) and subsequent colors
        # for walls, ball, blocks, etc
        tile = self.tiles[ (x, y) ]
        char = ' '
        if tile == 4:
            char = "B"
        elif tile == 3:
            char = '='
        if char == ' ':
            ansi_str = '{:c}[{};{}H{:c}[{}m{}'.format( 27, y+2, x+2, 27, 40 + tile, char )
        else:
            ansi_str = '{:c}[{};{}H{}'.format( 27, y+2, x+2, char )
        print(ansi_str, end='', flush=True)

        ansi_str = '{:c}[0;0H{}'.format( 27, self.score )
        print(ansi_str, end='', flush=True)

    def start(self):
        # start the int computer
        self._computer = IntComputer.IntComputer( self._program, self._input_queue, self._output_queue )
        threading.Thread( target = self._computer.run).start( )

        # keep track of paddle and ball
        paddle_x = -1
        ball_x = -1

        while self._computer.is_running is True:
            outputs = [ ]
            for _ in range(3):
                outputs.append( self._output_queue.get( ) )
                
            # deal with the output
            x = outputs.pop(0)
            y = outputs.pop(0)
            tile = outputs.pop(0)
            # remove empty tiles from the grid
            if tile == 0:
                self.tiles.pop( (x, y), None)
            elif tile == 3:
                paddle_x = x
            elif tile == 4:
                ball_x = x

                # I think that this works based on the way
                # the program works.  Trial and error
                # worked here :)
                self._input_queue.put( ball_x - paddle_x )
            
            if x == -1 and y == 0:
                self.score = tile
            else:
                self.tiles[ (x, y) ] = tile
                self._print_display( x, y )

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program =  [ int(x) for x in f.read().split(',') ]

    # part 1
    arcade = Arcade( program, False )
    arcade.start( )
    print ( len( [ x for x in arcade.tiles.values() if x == 2 ] ) )

    # part 2
    program[0] = 2
    arcade = Arcade( program, True )
    arcade.start( )
    print( arcade.score )
