from aocd.models import Puzzle

puzzle = Puzzle(year=2022, day = 10)
data =  puzzle.input_data

acc_vals = []
acc = 1
for l in data.splitlines():
    acc_vals.append(acc)
    if l.startswith('addx'):
        acc_vals.append(acc)
        acc += int(l.split()[1])

acc_vals.append(acc)
print(sum( [acc_vals[x] * (x+1) for x in range(19, len(acc_vals), 40)]))

pixels = [ '#' if (cycle % 40) in range(x-1,x+2) else '.' for cycle, x in enumerate(acc_vals)  ]
for start in range(0, len(pixels), 40):
    print(''.join(pixels[start:start+40]))

