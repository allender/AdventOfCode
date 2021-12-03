from aocd import lines
import functools

test_lines = [
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010',
]

def list_to_num(l):
    return int(''.join([str(i) for i in l]), 2)

def get_bit_lists(data):
    most_common_list = []
    least_common_list = []
    for i in range(len(data[0])):
        l = [ int(item[i]) for item in data ]
        
        # adds all the ones in the list.  mulitply by 2 because we
        # want to know if we have more 1's or 0's.  Multiplying
        # by 2 will tell us if we have more 1s than 0s in the list
        num_found = sum(l) * 2
        which_bit = int(-1 if num_found == len(data) else num_found > len(data) )
        most_common_list.append(which_bit)
        least_common_list.append(int(not which_bit))

    return most_common_list, least_common_list

def part1(data):
    m, l = get_bit_lists(data)
    gamma = list_to_num(m)
    epsilon = list_to_num(l)
    return gamma * epsilon

def find_numbers(data, find_most, bit_pos):
    if find_most == True:
        counts, _ = get_bit_lists(data)
    else:
        _, counts = get_bit_lists(data)

    new_list = [] 
    for i in range(len(data)):
        if int(data[i][bit_pos]) == counts[bit_pos]:
            new_list.append(data[i])
        elif counts[bit_pos] == -1 and int(data[i][bit_pos]) == int(find_most):
            new_list.append(data[i])

    return new_list 

def part2(data):
    olist = data
    co2list = data

    which_bit = 0
    while (len(olist) > 1):
        olist = find_numbers(olist, True, which_bit)
        which_bit += 1

    oxygen = list_to_num(olist[0])

    which_bit = 0
    while (len(co2list) > 1):
        co2list = find_numbers(co2list, False, which_bit)
        which_bit += 1

    co2 = list_to_num(co2list)

    return oxygen * co2

if __name__ == '__main__': 
    print(part1(lines))
    print(part2(lines))
