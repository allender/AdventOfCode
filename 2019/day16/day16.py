# pylint: disable=missing-docstring, unused-import, mixed-indentation
import sys
import os

if __name__ == '__main__':
    filename = 'input.txt'
    with open(filename) as f:
        number = [ int (x) for x in f.read().strip() ]

    default_pattern = ( 0, 1, 0, -1 )

    # part 1
    length = len(number)
    working_number = number[:]
    # for _ in range(100):
    #     for j in range(length):
    #         s = 0
    #         for i in range(length):
    #             pattern_val = default_pattern[ (i+1) // (j+1) % 4 ]
    #             s += (pattern_val * working_number[i])
    #         working_number[j] = abs(s) % 10

    #print (''.join(str(x) for x in working_number[:8]))

    # part 2
    offset = int(''.join(map(str, number[:7])))
    working_number = (number*10000)[offset:]
    for _ in range(100):
        s = 0
        for i in range(len(working_number) - 1, -1, -1):
            s += working_number[i]
            working_number[i] = s % 10
    
    print(''.join(str(x) for x in working_number[:8]))