# pylint: disable=missing-docstring, unused-import, mixed-indentation
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from IntComputer import IntComputer

class Arcade(IntComputer.IntComputer):

    def __init__(self, program):
        self._program = program
        self.tiles = { }
        self.score = 0
        self.paddle_x = -1 
        self.ball_x = -1 
        super().__init__(program)

    def run(self):
        self.is_running = True
        while(True):
            self.run_instruction( )

            # deal with the output
            if len(self.outputs) == 3:
                while self.outputs:
                    x = self.outputs.pop(0)
                    y = self.outputs.pop(0)
                    tile = self.outputs.pop(0)
                    # remove empty tiles from the grid
                    if tile == 0:
                        self.tiles.pop( (x, y), None)
                    elif tile == 3:
                        self.paddle_x = x
                    elif tile == 4:
                        self.ball_x = x
                    
                    if x == -1 and y == 0:
                        self.score = tile
                        ansi_str = '{:c}[0;0H{}'.format( 27, tile )
                        print(ansi_str, end='', flush=True)
                    else:
                        self.tiles[ (x, y) ] = tile

                        # use ansi color to print out the board.  Use the background
                        # colors in order from 40 (black) and subsequent colors
                        # for walls, ball, blocks, etc
                        ansi_str = '{:c}[{};{}H{:c}[{}m '.format( 27, y+1, x+1, 27, 40 + tile )
                        print(ansi_str, end='', flush=True)

                # see if we should set the input for the joystick
                self.steady_input = self.ball_x - self.paddle_x

            if (self.is_running == False):
                break


if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        program = f.read()

    # part 1
    arcade = Arcade( program )
    arcade.run( )
    print ( len( [ x for x in arcade.tiles.values() if x == 2 ] ) )

    # part 2
    arcade = Arcade( program )
    arcade.memory.set( 0, 2 )
    arcade.run( )
    print( arcade.score )


