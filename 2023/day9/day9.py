from aocd.models import Puzzle

puzzle = Puzzle(2023, 9)

input = puzzle.input_data.split('\n')
# input = puzzle.examples[0][0].split('\n')

def solve(seq):
    diffs = [ seq[x + 1] - seq[x] for x in range(len(seq) - 1) ]

    if all(diff == 0 for diff in diffs):
        seq.insert(0, seq[-1])
        seq.append(seq[-1])
        return seq
    
    new_seq = solve(diffs)
    seq.insert(0, seq[0] - new_seq[0])
    seq.append(seq[-1] + new_seq[-1])
    return seq


totals = [ solve(list(map(int, l.split()))) for l in input ]
print(sum([x[-1] for x in totals]))
print(sum([x[0] for x in totals]))