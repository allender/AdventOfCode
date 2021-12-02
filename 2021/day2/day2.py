from aocd import lines
from dataclasses import dataclass

@dataclass
class Instruction:
    dir : str
    count : int

def part1(instructions):
    h = 0
    v = 0
    for i in instructions:
        if i.dir[0] == 'f':
            h += i.count
        elif i.dir[0] == 'd':
            v += i.count
        elif i.dir[0] == 'u':
            v -= i.count

    return h * v

def part2(instructions):
    h = 0
    v = 0
    a = 0
    for i in instructions:
        if i.dir[0] == 'f':
            h += i.count
            v += (a * i.count)
        elif i.dir[0] == 'd':
            a += i.count
        elif i.dir[0] == 'u':
            a -= i.count

    return h * v
if __name__ == '__main__': 
    instructions = []
    for l in lines:
        x = l.split(' ')
        instructions.append(Instruction(x[0], int(x[1])))

    print(part1(instructions))
    print(part2(instructions))