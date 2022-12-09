from aocd.models import Puzzle
from aocd import lines
from collections import namedtuple

puzzle = Puzzle(year=2022, day = 9)

test_data = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''

test_data2 = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''

Position = namedtuple('Positon', ['x', 'y'])

MOVE_DIRECTIONS = {
    'L': Position( -1, 0),
    'R': Position(1, 0),
    'U': Position(0, 1),
    'D': Position(0, -1),
}

ADJACENT_LOCATIONS = [
    Position(-1, 1),
    Position(0, 1),
    Position(1, 1),
    Position(-1, 0),
    Position(0, 0),
    Position(1, 0),
    Position(-1, -1),
    Position(0, -1),
    Position(1, -1)
]

def move_head(rope, dir):
    new_rope =  [ Position(rope[0].x + MOVE_DIRECTIONS[dir].x, rope[0].y + MOVE_DIRECTIONS[dir].y) ]
    new_rope.extend(rope[1:])
    return new_rope

# move the fail to be next to the head
def move_tail(rope):
    # see if the tail has to move
    new_rope = [ rope[0] ]
    for index,tail in enumerate(rope[1:]):
        tail_x = tail.x 
        tail_y = tail.y
        check_positions = [ Position(new_rope[index].x + pos.x, new_rope[index].y + pos.y) for pos in ADJACENT_LOCATIONS ]
        if tail not in check_positions:
            if tail.x < new_rope[index].x:
                tail_x = tail.x + 1
            elif tail.x > new_rope[index].x:
                tail_x = tail.x - 1

            if tail.y < new_rope[index].y:
                tail_y = tail.y + 1
            elif tail.y > new_rope[index].y:
                tail_y = tail.y - 1

        new_rope.append(Position(tail_x, tail_y))

    return new_rope

def move_rope(data, tail_length):
    rope = [ Position(0,0) for _ in range(tail_length + 1)]
    tail_locations = [ rope[-1] ]

    for l in data.splitlines():
        dir, count = l.split()
        for _ in range(int(count)):
            rope = move_head(rope, dir)
            rope = move_tail(rope)
            tail_locations.append(rope[-1])

    unique_tail_locations = set(tail_locations)
    print(len(unique_tail_locations))

data = puzzle.input_data 
move_rope(data, 1)
move_rope(data, 9)
