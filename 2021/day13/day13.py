from aocd import lines
from typing import List, Tuple
from collections import defaultdict

test_lines = [
    '6,10',
    '0,14',
    '9,10',
    '0,3',
    '10,4',
    '4,11',
    '6,0',
    '6,12',
    '4,1',
    '0,13',
    '10,12',
    '3,4',
    '3,0',
    '8,4',
    '1,10',
    '2,14',
    '8,10',
    '9,0',
    '',
    'fold along y=7',
    'fold along x=5'
]
def parse_lines(lines: List) -> Tuple[dict, List]:
    points = defaultdict(int)
    folds = []
    for l in lines:
        if l.startswith('fold along y='):
            folds.append(('y', int(l.split('=')[1])))
        elif l.startswith('fold along x='):
            folds.append(('x', int(l.split('=')[1])))
        elif l != '':
            x, y = map(int, l.split(','))
            points[(x,y)] = '#' 

    return points, folds

def fold_paper(graph:dict, folds:List, part1 = True) -> int:
    for d, val in folds:
        keys_to_add = []
        keys_to_delete = [] 
        for (x,y) in graph.keys():
            # if the y value is less that the y_fold and it's 
            # a point, move it ot the right spot and then delete
            # the key
            if d == 'y' and y > val:
                new_y = val - (y - val)
                assert(new_y < val)
                keys_to_add.append((x, new_y)) 
                keys_to_delete.append((x, y))
            elif d == 'x' and x > val:
                new_x = val - (x - val)
                assert(new_x < val)
                keys_to_add.append((new_x, y)) 
                keys_to_delete.append((x, y))

        for k in keys_to_delete:
            del graph[k]

        for k in keys_to_add:
            graph[k] = '#'

        if part1 == True:
            print(len(graph.keys()))
            part1 = False

    # print out the numbers that are left in the
    # graph
    maxx = max( [ x for (x,y) in graph.keys() ] )
    maxy = max( [ y for (x,y) in graph.keys() ] )
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if (x,y) in graph and graph[(x,y)] == '#':
                print('#', end='')
            else:
                print(' ', end='')
        print('')


if __name__ == '__main__': 
    graph, folds = parse_lines(lines)
    fold_paper(graph, folds)
