from aocd.models import Puzzle

puzzle = Puzzle(2023, 13)

input = puzzle.input_data.split('\n\n')
# input = puzzle.examples[0][0].split('\n\n')

mirrors = [ l.split('\n') for l in input ]

# determines which horizontal index about which we have symmetry.  Taking
# advantage of the fact that you can't have symmetry around 0
def find_symmetry(p, num_diffs_allowed):
    for index in range(1, len(p)):
        s = sum( [ 0 if c1==c2 else 1 for l1, l2 in zip(p[index - 1::-1], p[index:]) for c1, c2 in zip(l1, l2) ] )
        if s == num_diffs_allowed:
            return index
    
    return 0

def find_mirror(p, num_diffs_allowed):
    # try and find mirror on horizontals.  
    horiz = find_symmetry(p, num_diffs_allowed)
    if horiz > 0:
        return 100 * horiz

    # transpose the list    
    horiz = find_symmetry( [ ''.join(x) for x in zip(*p)], num_diffs_allowed )
    if horiz >= 0:
        return horiz

    assert(0)

total = 0
total1 = 0
for p in mirrors:
    total += find_mirror(p, 0)
    total1 += find_mirror(p, 1)

print(total, total1)
