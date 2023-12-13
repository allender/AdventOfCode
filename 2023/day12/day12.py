from aocd.models import Puzzle

puzzle = Puzzle(2023, 12)

input = puzzle.input_data.split('\n')
# input = puzzle.examples[0][0].split('\n')
# input = '''???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1'''.split('\n')

class Spring():
    def __init__(self, input):
        self.pattern = input.split(' ')[0]
        self.sequence_str = input.split()[1]
        self.sequences = [ int(s) for s in input.split()[1].split(',') ]

    def calc_possibilities(self, cur_pos, cur_sequence, cur_unknown_count, cache):
        h = hash((cur_pos, cur_sequence, cur_unknown_count))
        if h in cache:
            return cache[h]

        # at the end of the pattern, we are done
        if cur_pos == len(self.pattern) and cur_sequence == len(self.sequences) and cur_unknown_count == 0:
            return 1
        elif cur_pos == len(self.pattern) and cur_sequence == len(self.sequences) - 1 and self.sequences[cur_sequence] == cur_unknown_count:
            return 1
        elif cur_pos == len(self.pattern):
            return 0

        val = 0

        # pattern match against a '.'
        if self.pattern[cur_pos] == '.' or self.pattern[cur_pos] == '?':
            if cur_unknown_count == 0:
                val += self.calc_possibilities(cur_pos + 1, cur_sequence, 0, cache)
            elif cur_unknown_count > 0 and cur_sequence < len(self.sequences) and self.sequences[cur_sequence] == cur_unknown_count:
                val += self.calc_possibilities(cur_pos + 1, cur_sequence + 1, 0, cache)

        # pattern match against a #
        if self.pattern[cur_pos] == '#' or self.pattern[cur_pos] == '?':
            val += self.calc_possibilities(cur_pos + 1, cur_sequence, cur_unknown_count + 1, cache)

        cache[h] = val
        return val
        
    def __repr__(self):
        return self.pattern + ' ' + str(self.sequences)

springs = [ Spring(l) for l in input ]

# print(sum(x.calc_possibilities(0, 0, 0) for x in springs))

# part 2
for s in springs:
    s.pattern = '?'.join([ s.pattern, s.pattern, s.pattern, s.pattern, s.pattern ])
    s.sequences = [ int(x) for x in ','.join([ s.sequence_str, s.sequence_str, s.sequence_str, s.sequence_str, s.sequence_str ]).split(',')]
    # print(s)

print(sum(x.calc_possibilities(0, 0, 0, {}) for x in springs))
