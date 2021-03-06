import sys
import math
import re

sys.path.append('../..')

import utils

test_data = """939
7,13,x,x,59,x,31,19"""

if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')
    my_time = int(data[0])

    bus_numbers = [ int(x) for x in data[1].split(',') if x != 'x' ]
    bus_schedule = [ (int(x), i) for i, x in enumerate(data[1].split(',')) if x != 'x' ]
    remainders = [ math.modf(my_time / x) for x in bus_numbers ]

    index = 9
    largest = 0.0
    for i,r in enumerate(remainders):
        if (r[0] > largest):
            index = i
            largest = r[0]
    print (bus_numbers[index] * (bus_numbers[index] * int(remainders[index][1]+1) - my_time))

    cur_bus = 0
    bus_number = bus_schedule[cur_bus][0]
    next_time = bus_schedule[cur_bus][1]
    start_time = 1
    delta = 1
    while True:
        if (start_time + next_time) % bus_number != 0:
            start_time += delta
        else:
            delta *= bus_schedule[cur_bus][0]
            cur_bus += 1
            if cur_bus == len(bus_schedule):
                break
            bus_number = bus_schedule[cur_bus][0]
            next_time = bus_schedule[cur_bus][1]

    print (start_time)
 
