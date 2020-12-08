import sys
from collections import defaultdict

sys.path.append('../..')

import utils

test_data = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

class BadOpcode(Exception):
    def __init__(self, message):
        self.message = message

class InfiniteLoop(Exception):
    def __init__(self, message):
        self.message = message

class Opcode():
    def __init__(self, opcode, operand):
        self.operand = operand
        self.opcode = opcode
        self.visited = False

class Handheld():
    def __init__(self, program_text):
        self.program = []
        for line in program_text:
            if len(line) == 0:
                continue

            l = line.split(' ')
            self.program.append(Opcode(l[0], int(l[1])))

        self.reset()

    def reset(self):
        self.pc = 0
        self.acc = 0
        self.pc = 0
        for l in self.program:
            l.visited = False

    def inc_acc(self, val):
        self.acc += val
        self.pc += 1

    def jump(self, offset):
        self.pc += offset

    def nop(self):
        self.pc += 1

    def step(self):
        opcode = self.program[self.pc]
        if (opcode.visited == True):
            # infinite loop
            raise InfiniteLoop("Infinate loop detected  pc:{0}  acc: {1}".format(self.pc, self.acc))

        if (opcode.opcode == 'acc'):
            self.inc_acc(opcode.operand)
        elif (opcode.opcode == 'jmp'):
            self.jump(opcode.operand)
        elif (opcode.opcode == 'nop'):
            self.nop()
        else:
            raise BadOpcode("Opcode {0} not found".format(opcode.opcode))

        opcode.visited = True
        if (self.pc >= len(self.program)):
            return True

        return False

def find_reachable(graph, instruction, visited = None):
    if visited == None:
        visited = set()
    visited.add(instruction)

    found = set()
    for child in graph[instruction]:
        if child not in visited:
            found |= find_reachable(graph, child, visited)

    return found | { instruction }
            
def find_instruction(from_start, from_end, program):
    for pc in from_start:
        if (program[pc].opcode == 'nop') and program[pc + program[pc].operand] in from_end:
            return pc
        elif (program[pc].opcode == 'jmp') and pc + 1 in from_end:
            return pc


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read()

    data = data.split('\n');

    handheld = Handheld(data)

    done = False
    while(done == False):
        try:
            done = handheld.step()

        except Exception as e:
            print(e)
            break

    print(handheld.acc)

    # part 2 - build set of reachable nodes from the start
    # and reachable nodes when going from the end and then
    # find out where we need to insert instruction to
    # allow us to go from start to end

    forward_set = defaultdict(set)
    reverse_set = defaultdict(set)
    program_len = len(handheld.program)
    for i, opcode in enumerate(handheld.program):
        if (opcode.opcode == 'jmp'):
            target = i + opcode.operand
        else:
            target = i + 1
        
        forward_set[i].add(target)
        reverse_set[target].add(i)

    # find all of the nodes we can get to from the beginning and from the end
    reachable_from_start = find_reachable(forward_set, 0)
    reachable_from_end = find_reachable(reverse_set, program_len)

    # with the set of nodes that we can reach from the beginning and the
    # end we can now figure out which node in the "from_start" which is 
    # a nop or jump will get us to one of the nodes in the reachable_from_end
    # set
    swap_instruction = find_instruction(reachable_from_start, reachable_from_end, handheld.program)
    handheld.program[swap_instruction].opcode = ('jmp' if handheld.program[swap_instruction].opcode == 'nop' else 'nop')

    handheld.reset()
    done = False
    while(done == False):
        try:
            done = handheld.step()

        except Exception as e:
            print(e)
            break

    print(handheld.acc)


