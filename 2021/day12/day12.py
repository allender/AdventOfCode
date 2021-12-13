from aocd import lines
from typing import List, Tuple
from collections import defaultdict

import sys
sys.path.append('../..')
import utils

test_small = [ 
    'start-A',
    'start-b',
    'A-c',
    'A-b',
    'b-d',
    'A-end',
    'b-end'
]

test_med = [
    'dc-end',
    'HN-start',
    'start-kj',
    'dc-start',
    'dc-HN',
    'LN-dc',
    'HN-end',
    'kj-sa',
    'kj-HN',
    'kj-dc'
]

def parse_lines(lines: str) -> dict:
    d = defaultdict(list)
    for l in lines:
        s, e = l.split('-')

        # make edges, but don't go back through start
        if e != 'start':
            d[s].append(e)
        if s != 'start':
            d[e].append(s)

    return d

def find_paths_from(paths: dict, cave: str, visited: set, backtrack: bool) -> int:
    # if at the end, then return 1 for the count 
    # and no more procession
    if cave == 'end':
        return 1

    #determine count from this position
    path_length = 0
    for c in paths[cave]:
        # if we have an upper case, just keep working on a path, but
        # don't include the upper case cave as visited since we
        # can visit them more than ones
        if c.isupper():
            path_length += find_paths_from(paths, c, visited, backtrack)

        # otherwise it's lower case and we haven't visited, so put 
        # current cave into the visited set and keep working
        elif c not in visited:
            path_length += find_paths_from(paths, c, visited | {c}, backtrack)
        
        # again, this is a lower case cave and it's already been visited
        # once, so fallback to the mode where we can't visit smaller case
        # caves more than once by making backtrack = True
        elif backtrack == True: 
            path_length += find_paths_from(paths, c, visited, False)

    return path_length
            

@utils.func_timer
def find_paths(paths: dict, backtrack = False) -> int:
    return find_paths_from(paths, 'start', set(['start']), backtrack )

if __name__ == '__main__': 
    paths = parse_lines(lines)
    print(find_paths(paths, False))
    print(find_paths(paths, True))
