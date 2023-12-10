from aocd.models import Puzzle

puzzle = Puzzle(2023, 6)

mappings = puzzle.input_data.split('\n')
# mappings = puzzle.examples[0][0].split('\n')
times = map(int, mappings[0].split()[1:])
distances = map(int, mappings[1].split()[1:])

def calculate_total(distances, times):
    total = 1
    for d, t in zip(distances, times):
        calculated_distances = []
        for i in range(t + 1):
            calculated_distances.append((t - i) * i)

        count = 0
        for i in calculated_distances:
            if i > d:
                count += 1

        total  *= count

    return total


print(calculate_total(distances, times))

part2_time = int(mappings[0].split(':')[1:][0].replace(' ',''))       
part2_distance = int(mappings[1].split(':')[1:][0].replace(' ',''))        

print (calculate_total([part2_distance], [part2_time]))