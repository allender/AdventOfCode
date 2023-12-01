from aocd.models import Puzzle

puzzle = Puzzle(2023, 1)
lines = puzzle.input_data.splitlines()

subs = {
    'one' : 'o1e',
    'two' : 'to2o',
    'three' : 't3e',
    'four' : 'f4r',
    'five' : 'f5e',
    'six' : 's6x',
    'seven' : 's7n',
    'eight' : 'e8t',
    'nine' : 'n9e'
}

def part1():
    total = 0
    for l in lines:
        digits = [ x for x in l if x.isdigit() ]
        num = int(digits[0] + digits[-1])
        total += num 
    print(total)

def part2():
    total = 0
    for l in lines:
        for k,v in subs.items():
            l = l.replace(k,v)
        digits = [ x for x in l if x.isdigit() ]
        num = int(digits[0] + digits[-1])
        total += num 
    print(total)
        
part1()
part2()

