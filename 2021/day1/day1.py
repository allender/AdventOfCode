from aocd import numbers

def part1(data):
    increases = 0
    for i in range(1, len(data)):
        if data[i] > data[i-1]:
            increases = increases + 1

    return increases

def part2(data):
    sums = [ data[x] + data[x-1] + data[x - 2] for x in range(2, len(data)) ]
    return part1(sums)

if __name__ == '__main__':
    print(part1(numbers))
    print(part2(numbers))
