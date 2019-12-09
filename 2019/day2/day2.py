import sys


def run_program(opcodes):
    ip = 0
    while (True):
        opcode = opcodes[ip]
        num1 = opcodes[opcodes[ip + 1]]
        num2 = opcodes[opcodes[ip + 2]]
        dest = opcodes[ip + 3]
        if (opcode == 1):
            num3 = num1 + num2
        elif (opcode == 2):
            num3 = num1 *  num2
        elif (opcode == 99):
            break
        else:
            assert("bad juju")
        
        opcodes[dest] = num3
        ip += 4



if __name__ == '__main__':
    with open('input.txt') as f:
        s = f.read()

    orig_opcodes = [ int(x) for x in s.split(',') ]

    ip = 0
    values = range(0, 99)
    for x in values:
        for y in values: 
            opcodes = orig_opcodes.copy()
            opcodes[1] = x
            opcodes[2] = y
            run_program(opcodes)
            if (opcodes[0] == 19690720):
                print(opcodes)
                print (100 * opcodes[1] + opcodes[2])
                sys.exit(0)


