import sys
from aocd import lines
from typing import List 

test_lines = [
    '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1',
    '',
    '22 13 17 11  0',
    '8  2 23  4 24',
    '21  9 14 16  7',
    '6 10  3 18  5',
    '1 12 20 15 19',
    '',
    '3 15  0  2 22',
    '9 18 13 17  5',
    '19  8  7 25 23',
    '20 11 10 24  4',
    '14 21 16 12  6',
    '',
    '14 21 17 24  4',
    '10 16 15  9 19',
    '18  8 23 26 20',
    '22 11 13  6  5',
    '2  0 12  3  7'
 ]

class Board():
    class Slot():
        def __init__(self, number):
            self.number = number
            self.picked = False

        def pick(self, number):
            if (self.number == number):
                self.picked = True
            return self.picked

    def __init__(self, lines: List):
        self.lines = []
        self.unmarked_sum = 0
        self.won = False
        for l in lines:
            numbers = [ int(x) for x in l.replace('  ', ' ').strip().split(' ') ]
            slots = [ self.Slot(n) for n in numbers ]
            self.lines.append(slots)

            # calculate the entire unmarked total for the board so
            # that we will have the final value when the board wins
            # without having to recalculate it then
            self.unmarked_sum += sum( [s.number for s in slots] )

        # set the size of the board for easier iteration
        self.size = len(self.lines[0])

    # build up a row dynamically - this could stored
    def get_row(self, num) -> List:
        return [ x for x in self.lines[num] ]

    # build up a column dynamically - this could stored
    def get_column(self, num) -> List:
        column = []
        for r in range(self.size):
            column.append(self.lines[r][num])
        return column

    # returns true if the gievn row is complete, false otherwise
    def row_complete(self, num):
        row = self.get_row(num)
        return all( x.picked == True for x in row )

    # returns true if the gievn volume is complete, false otherwise
    def column_complete(self, num):
        column = self.get_column(num)
        return all( x.picked == True for x in column )

    # checks a number to see if it's on the board
    def check_number(self, number):
        for l in self.lines:
            for s in l:
                if s.picked == False and s.pick(number) == True:
                    self.unmarked_sum -= s.number
                    break

        # see if there is a win condition on the board
        for i in range(self.size):
            if self.row_complete(i) == True:
                self.won = True
            elif self.column_complete(i) == True:
                self.won = True
            if self.won == True:
                break

def parse_boards(lines):
    current_line = 0
    numbers = lines[current_line]
    current_line += 1
    boards = []
    while current_line < len(lines):
        current_line += 1    # skip blank line
        board_numbers = []
        for _ in range(5):
            board_numbers.append(lines[current_line])
            current_line += 1
        boards.append(Board(board_numbers))

    return numbers, boards

def solve(numbers, boards, part1):
    for number in [ int(x) for x in numbers.split(',') ]:
        for b in boards:
            b.check_number(number)
            if b.won == True and part1 == True:
                return b.unmarked_sum * number
            if b.won == True and sum ([ int(x.won) for x in boards ]) == len(boards):
                return b.unmarked_sum * number

if __name__ == '__main__': 
    numbers, boards = parse_boards(lines)
    print(solve(numbers, boards, True))
    print(solve(numbers, boards, False))