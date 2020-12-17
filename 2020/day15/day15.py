import re
import time
from collections import defaultdict
import numpy

test_data = """0,3,6"""
test_data1 = """1,3,2"""
test_data2 = """2,1,3"""

input_data = """16,1,0,18,12,14,19"""

if __name__ == '__main__':
    data = input_data.split(',')

    start = time.time()
    timestamps = {}
    l = numpy.full((30000000), -1, dtype='int')

    last_num = -1 
    for turn, d in enumerate(data):
        if last_num != -1:
            l[last_num] = turn
            # timestamps[last_num] = turn 
        last_num = int(d)

    while True:
        turn += 1
        if turn == 30000000:
            print(last_num)
            break

        if turn == 2020:
            print(last_num)

        # last_time = timestamps.get(last_num, None)
        # if last_time == None:
        last_time = l[last_num]
        if last_time == -1:
            # timestamps[last_num] = turn
            l[last_num] = turn
            next_num = 0
        else:
            # next_num = turn - timestamps[last_num]
            # timestamps[last_num] = turn
            next_num = turn - l[last_num]
            l[last_num] = turn

        last_num = next_num
