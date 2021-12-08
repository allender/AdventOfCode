from aocd import lines
from typing import List
from functools import reduce

test_lines = [
    'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
    'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
    'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
    'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
    'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
    'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
    'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
    'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
    'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
    'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce',
]

# for part1 to determine if a code contains a unique
# number of segments (1, 4, 7, and 8, which contain
# 2, 4, 3, and 7 segments respecitvely)
unique_counts = [ 2, 3, 4, 7 ]

if __name__ == '__main__': 
    easy_digit_count = 0
    total = 0
    for l in lines:
        patterns, digits = [ x.strip() for x in l.split('|') ]
        pattern_list = [ set(pattern) for pattern in patterns.split(' ') ]
        digits_list = [ set (digit) for digit in digits.split(' ') ]

        #easy_digit_count += part1( [ d for d in digits.split(' ') ] )
        easy_digit_count += sum( [ 1 for digit in digits.split(' ') if len(digit) in unique_counts ] )
        
        # array to store which pattern is which digit.  Since we are using
        # sets, the sets will all hash the same way even if the order
        # of the letters in the digit are different.  This array then
        # holds the paterm of 0, 1, ..., 9
        digit_patterns = [None] * 10

        digit_patterns[1] = [ d for d in pattern_list if len(d) == 2][0]
        digit_patterns[4] = [ d for d in pattern_list if len(d) == 4][0]
        digit_patterns[7] = [ d for d in pattern_list if len(d) == 3][0]
        digit_patterns[8] = [ d for d in pattern_list if len(d) == 7][0]

        # make a list of digits with 6 segments
        digits_069 = [digit for digit in pattern_list if len(digit) == 6]
        digit_patterns[6] = [ d for d in digits_069 if len(d & digit_patterns[7]) == 2 ][0]
        digit_patterns[9] = [ d for d in digits_069 if len(d & digit_patterns[4]) == 4 ][0]
        digit_patterns[0] = [ d for d in digits_069 if d != digit_patterns[9] and d != digit_patterns[6] ][0]
        
        # make a list of digits with 5 segments
        digits_235 = [digit for digit in pattern_list if len(digit) == 5]
        digit_patterns[3] = [ d for d in digits_235 if len(d & digit_patterns[1]) == 2 ][0]
        digit_patterns[5] = [ d for d in digits_235 if len(d & digit_patterns[6]) == 5 ][0]
        digit_patterns[2] = [ d for d in digits_235 if d != digit_patterns[3] and d != digit_patterns[5] ][0]
        
        assert(len(digit_patterns) == 10)

        # sum up the digit for part2
        total += reduce(lambda acc, digit: 10 * acc + digit_patterns.index(digit), digits_list, 0)

    print(easy_digit_count)
    print(total)


