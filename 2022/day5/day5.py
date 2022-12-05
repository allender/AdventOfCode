from aocd.models import Puzzle
from aocd import lines

puzzle = Puzzle(year=2022, day = 5)

# parse out the crate information
# figure out how many stacks we have
l = lines[0]
stacks_p1 = [ [] for i in range(0, len(l), 4)]
stacks_p2 = [ [] for i in range(0, len(l), 4)]

parsing_stacks = True 
for l in lines:
    if parsing_stacks == True:
        data = [ l[i:i+4].strip() for i in range(0, len(l), 4)]

        # stop processing when we get to stack numbers
        if data[0].isnumeric() == True:
            parsing_stacks = False
            continue

        for stack_number, crate in enumerate(data):
            if crate != '':
                stacks_p1[stack_number].insert(0, crate[1])
                stacks_p2[stack_number].insert(0, crate[1])

    elif l:
        # here we are parsing the movements.   Subtract 1 from start/end
        # because we are zero based
        p = l.split()
        count = int(p[1])
        start = int(p[3]) - 1
        end = int(p[5]) - 1
        part2_temp = []
        for _ in range(count):
            stacks_p1[end].append(stacks_p1[start].pop())
            part2_temp.append(stacks_p2[start].pop())

        for _ in range(count):
            stacks_p2[end].append(part2_temp.pop())

for stack in stacks_p1:
    print(stack[-1], end='')
print('')

for stack in stacks_p2:
    print(stack[-1], end='')
print('')
