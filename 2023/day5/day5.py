from aocd.models import Puzzle

puzzle = Puzzle(2023, 5)
mappings = puzzle.input_data.split('\n\n')
# mappings = puzzle.examples[0][0].split('\n\n')
part1_seeds = [ (int(n),1) for n in mappings[0].split()[1:] ]
part2_seeds = [ (int(s), int(l)) for s, l in zip(mappings[0].split()[1::2], mappings[0].split()[2::2]) ]

def apply_mappings(seeds):
    for mapping in mappings[1:]:
        range_map = [ list(map(int, l.split())) for l in mapping.splitlines()[1:] ]

        new_seed_ranges = []
        for seed_start, seed_length in seeds:
            while seed_length > 0:
                found = False
                max_length = seed_length

                for dst, src, range in range_map:
                    if src <= seed_start < src + range:
                        src_dist = seed_start - src 
                        remaining_dist = min(range - src_dist, seed_length)
                        new_seed_ranges.append((dst + src_dist, remaining_dist))
                        seed_start += remaining_dist
                        seed_length -= remaining_dist
                        found = True
                        break
                    elif seed_start < src:
                        max_length = min(src - seed_start, max_length)

                if found == False:
                    remaining_length = min(max_length, seed_length)
                    new_seed_ranges.append((seed_start, remaining_length))
                    seed_length -= remaining_length
                    seed_start += remaining_length

        seeds = new_seed_ranges

    return seeds


print(min(x[0] for x in apply_mappings(part1_seeds)))
print(min(x[0] for x in apply_mappings(part2_seeds)))
