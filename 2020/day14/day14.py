import re
from collections import defaultdict

test_data = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

part2_data = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')
    mask_re = re.compile(r'mask = (?P<mask>[X01]{36})') 
    memory_re = re.compile(r'mem\[(?P<memory>\d+)\] = (?P<value>\d+)$')

    # part 1 - just grab the mask and values and
    # use some zip/list magic to put it all together
    memory = defaultdict(int)
    for l in data:
        mo = mask_re.match(l)
        if mo:
            mask = mo.group('mask') 

        mo = memory_re.match(l)
        if mo:
            # make mask and value the same width so that we can iterate
            # with 'zip' to determine the final value
            val = bin(int(mo.group('value')))[2:].zfill(len(mask))
            values = [ v if m == 'X' else m for v, m in zip(val, mask) ]
            value = int(''.join(values), 2)
            memory[int(mo.group('memory'))] = value

    print(sum(memory.values()))

    # for part two, do something simlar as above
    # but we can use python string formatting to
    # compute the string of the final address
    data = input_data.split('\n')
    memory = defaultdict(int)
    for l in data:
        mo = mask_re.match(l)
        if mo:
            mask = mo.group('mask') 

        mo = memory_re.match(l)
        if mo:
            dest_addr_fmt = '' 
            num_floating = 0
            address = bin(int(mo.group('memory')))[2:].zfill(len(mask))
            for a, m in zip(address, mask):
                if m == '1':
                    # becomes a 1
                    dest_addr_fmt += '1'
                elif m == '0':
                    # stays the same
                    dest_addr_fmt += a
                else:
                    # format element to put in a 1 or 0
                    dest_addr_fmt += '{' + str(num_floating) + '}'
                    num_floating += 1

            # with the format string, create addresses with
            # 0s and 1s in the adddress string and set the value
            for i in range(2 ** num_floating):
                addr_str = dest_addr_fmt.format(*bin(i)[2:].zfill(num_floating))
                address = int(addr_str, 2)
                memory[address] = int(mo.group('value'))

    print(sum(memory.values()))
