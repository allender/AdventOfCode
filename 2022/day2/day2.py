from aocd.models import Puzzle
from aocd import lines

puzzle = Puzzle(year=2022, day = 2)

# maps plays to score
possible_plays = {
    'AX' : 4,
    'AY' : 8,
    'AZ' : 3,
    'BX' : 1,
    'BY' : 5,
    'BZ' : 9,
    'CX' : 7,
    'CY' : 2,
    'CZ' : 6,
}

# maps part 2 meaning of XYZ to original plays
part2_map = {
    'AX' : 'AZ',
    'AY' : 'AX',
    'AZ' : 'AY',
    'BX' : 'BX',
    'BY' : 'BY',
    'BZ' : 'BZ',
    'CX' : 'CY',
    'CY' : 'CZ',
    'CZ' : 'CX',
}

moves = []
for l in lines:
    play, response = l.split()
    moves.append(play+response)

print (sum([ possible_plays[move] for move in moves]))
print (sum([ possible_plays[part2_map[move]] for move in moves]))
    