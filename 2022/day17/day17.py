from aocd.models import Puzzle
from itertools import cycle

puzzle = Puzzle(year=2022, day = 17)

ROCKS = [
    [ 0b0011110 ],

    [ 0b0001000,
      0b0011100,
      0b0001000 ],

     # upside down because we process from 0 - 2 in the list 
    [ 0b0011100,
      0b0000100,
      0b0000100 ],
      
    [ 0b0010000,
      0b0010000,
      0b0010000,
      0b0010000 ],

    [ 0b0011000,
      0b0011000 ]
]

NUM_ROCKS = len(ROCKS)

test_data = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''

# set up cyclic iterators for rocks and wind data
rock_iter = cycle(ROCKS)
wind_iter = cycle(test_data)

rows = [ 0b111111111 ]

def print_grid():
    for r in reversed(rows):
        for i in range(8, -1, -1):
            if r & 1 << i:
                print('#', end='')
            else:
                print('.', end = '')
        print('')
    print('\n')

def move_rock(rock, direction, y):
    # create bitmask with the rocks in the row and the walls 
    try:
        row = rows[y]
    except IndexError:
        row = 0

    if direction == '<':
        if not any((r & (1 << 7)) or ((r << 1) & row) for r in rock):
            return [ x << 1 for x in rock ]

    # right wall
    elif direction == '>':
        if not any((r & 1) or ((r >> 1) & row) for r in rock):
            return [ x >> 1 for x in rock ]

    # if we get here we collided against something
    return [ x for x in rock ]

def drop_rock(rock, cur_y):
    for index in range(len(rock)):
        try:
            if rock[index] & rows[cur_y + index - 1]:
                return False
        except IndexError:
            break

    return True
    
def do_simulation(wind_data, num_steps = 2022):
    for _ in range(num_steps):
        # simulate one rock dropping
        cur_rock = next(rock_iter)
        cur_y = len(rows) + 3
        while True:
            w = next(wind_iter)
            cur_rock = move_rock(cur_rock, w, cur_y)
            if drop_rock(cur_rock, cur_y) == False:
                break
            cur_y -= 1

        # rock can't drop, so stop processing this rock and then 
        # add in the rock to the current rows, and repeat
        for index in range(len(cur_rock)):
            try:
                rows[cur_y + index] |= cur_rock[index]
            except IndexError:
                rows.append(cur_rock[index])

do_simulation(test_data, 2022)
print(len(rows)-1)