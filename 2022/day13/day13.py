from aocd.models import Puzzle
import functools

puzzle = Puzzle(year=2022, day = 13)

test_data = '''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]'''

VALID = -1
INVALID = 1
UNKNOWN = 0

def compare_packets(left, right):
    pairs = list(zip(left, right))
    for l, r in pairs:
        if type(l) == int and type(r) == int:
            if l < r:
                return VALID
            elif l > r:
                return INVALID
    
        elif type(l) == int:
            assert(type(r) == list)
            return compare_packets([l], r)

        elif type(r) == int:
            assert(type(l) == list)
            return compare_packets(l, [r])

        else:
            # both type are lists.  run compare on each list
            result = compare_packets(l, r)
            if result == VALID or result == INVALID:
                return result


    # if left side ran out of items, this is valid
    if len(left) < len(right):
        return VALID
    elif len(left) > len(right):
        return INVALID

    return UNKNOWN

def parse_data(data):
    packets = []
    for l in data.splitlines():
        if l == '':
            continue
        packets.append(eval(l))

    return packets


data = puzzle.input_data
packets = parse_data(data)
sum = 0
for index in range(0, len(packets), 2):
    if compare_packets(packets[index], packets[index+1]) == VALID:
        sum += (index//2 + 1)
print(sum)

# for part 2, just compare packet to all ordered packets and stick it in
# the right place.  Just add the two signal packets in and go.  The compare_packets
# function above is used for the sort comparison function.  Return values
# picked to "do the right thing"
packets.append([[2]])
packets.append([[6]])

sorted_packets = sorted(packets, key=functools.cmp_to_key(compare_packets))
print((sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]])+ 1))