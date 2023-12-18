from aocd.models import Puzzle

puzzle = Puzzle(2023, 18)

inputs = puzzle.input_data.strip().split('\n')
# inputs = puzzle.examples[0][0].split('\n')

# maps character to direction
dir_map = {
    'R' : 1,
    'L' : -1,
    'U' : -1j,
    'D' : 1j,
}

hex_dir_map = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}

def find_area(instructions):
    current = complex(0, 0)
    path = [ current ]
    for dir,steps in instructions:
        for index in range(int(steps)):
            current += dir_map[dir]
            path.append(current)

    area = abs(0.5 * sum(a.real*b.imag - a.imag*b.real for a,b in zip(path, path[1:])))
    return area + (len(path)-1)//2 + 1

def calc_instructions(old_instructions):
    new_instructions = []
    for color in old_instructions:
        length = int(color[2:7], 16)
        dir = hex_dir_map[color[7]]
        new_instructions.append((dir, length))

    return new_instructions

steps = [ l.split(' ')[0:2] for l in inputs]
print(find_area(steps))
print(find_area(calc_instructions([ l.split(' ')[2] for l in inputs])))

