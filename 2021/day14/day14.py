from aocd import lines
from typing import List, Tuple
from collections import defaultdict

test_lines = [
    'NNCB',
'',
    'CH -> B',
    'HH -> N',
    'CB -> H',
    'NH -> C',
    'HB -> C',
    'HC -> B',
    'HN -> C',
    'NN -> C',
    'BH -> H',
    'NC -> B',
    'NB -> B',
    'BN -> B',
    'BB -> N',
    'BC -> B',
    'CC -> N',
    'CN -> C',
]

def parse_lines(lines: list) -> Tuple[str, dict]:
    mapping = defaultdict(str)
    chain = lines[0]
    for l in lines[2:]:
        pair, _, value = l.split(' ')
        mapping[pair] = value

    return chain, mapping

def part1(starting_chain: str, mapping: dict, iterations: int) -> int:
    current_pairs_count = defaultdict(int)
    for i in range(len(starting_chain) - 1):
        pair = starting_chain[i:i+2]
        current_pairs_count[pair] += 1

    for _ in range(iterations):
        new_pairs_count = defaultdict(int) 
        for pair, pair_count in current_pairs_count.items():
            insertion = mapping[pair]
            new_pairs_count[pair[0] + insertion] += pair_count
            new_pairs_count[insertion + pair[1]] += pair_count

        current_pairs_count = new_pairs_count

    # find the counts of the elements.  We can do this by looking
    # at the first element of the pair and then moving to the next
    # pair.  This works because the next pair in the list (if
    # we were to actually generated it) would be counted in another
    # pair in the map.  We must account for the last element as well
    element_count = defaultdict(int)
    for pair, pair_count in current_pairs_count.items():
        element_count[pair[0]] += pair_count
    element_count[starting_chain[-1]] += 1

    max_count = max( [ x for x in element_count.values() ] )
    min_count = min( [ x for x in element_count.values() ] )   
    return max_count - min_count

if __name__ == '__main__': 
    chain, mapping = parse_lines(lines)
    print(part1(chain, mapping, 10))
    print(part1(chain, mapping, 40))