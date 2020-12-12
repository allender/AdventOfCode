import sys
from collections import Counter
from collections import defaultdict

sys.path.append('../..')

import utils

test_data = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

def get_num_adj(data, x, y):
    num_adj = 0
    for i in range(max(0, x - 1), min(len(data), x + 2)):
        for j in range(max(0, y - 1), min(len(data[i]), y + 2)):
            if i == x and j == y:
                continue
            if data[i][j] == '#':
                num_adj += 1

    return num_adj 

def seen_in_direction(data, x, y, d):
    new_pos = (x + d[0], y + d[1])
    while new_pos[0] >= 0 and new_pos[0] < len(data) and new_pos[1] >= 0 and new_pos[1] < len(data[new_pos[0]]):
        if data[new_pos[0]][new_pos[1]] == '#':
            return 1
        elif data[new_pos[0]][new_pos[1]] == 'L':
            break
        new_pos = (new_pos[0] + d[0], new_pos[1] + d[1])
        
    return 0
            
def get_num_seen(data, x, y):
    dirs = [ (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1), ]
    num_seen = 0
    for d in dirs:
        num_seen += seen_in_direction(data, x, y, d)

    return num_seen

def get_num_seats(data):
    last_count = 0
    while True:
        seats_to_change = [ ]
        for x in range(len(data)): 
            for y in range(len(data[x])):
                spot = data[x][y]
                if spot == '.':
                    continue
                num_adj = get_num_adj(data, x, y)
                if num_adj == 0 and spot == 'L':
                    seats_to_change.append((x, y, '#'))
                elif num_adj >= 4 and spot == '#':
                    seats_to_change.append((x, y, 'L'))

        if not seats_to_change:
            return sum(map(lambda s: s.count('#'), data))

        for seat in seats_to_change:
            data[seat[0]][seat[1]] = seat[2] 

def get_num_seats_part2(data):
    last_count = 0
    while True:
        seats_to_change = [ ]
        for x in range(len(data)): 
            for y in range(len(data[x])):
                spot = data[x][y]
                if spot == '.':
                    continue
                num_adj = get_num_seen(data, x, y)
                if num_adj == 0 and spot == 'L':
                    seats_to_change.append((x, y, '#'))
                elif num_adj >= 5 and spot == '#':
                    seats_to_change.append((x, y, 'L'))

        if not seats_to_change:
            return sum(map(lambda s: s.count('#'), data))

        for seat in seats_to_change:
            data[seat[0]][seat[1]] = seat[2] 


if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = list(map(list, input_data.split('\n')))
    num_seats = get_num_seats(data)
    print(num_seats)
    data = list(map(list, input_data.split('\n')))
    num_seats = get_num_seats_part2(data)
    print(num_seats)