from aocd import lines
from typing import Tuple

test_lines = [
    '[({(<(())[]>[[{[]{<()<>>',
    '[(()[<>])]({[<{<<[]>>(',
    '{([(<{}[<>[]}>{[]{[(<()>',
    '(((({<>}<{<{<>}{[]{[]{}',
    '[[<[([]))<([[{}[[()]]]',
    '[{[{({}]{}}([{[{{{}}([]',
    '{<[[]]>}<{[{[{[]{()[[[]',
    '[<(<(<(<{}))><([]([]()',
    '<{([([[(<>()){}]>(<<{{',
    '<{([{{}}[<[[[<>{}]]]>[]]',
]

open_chars = [ '(', '[', '{', '<' ]
close_chars = [ ')', ']', '}', '>' ]
error_vals = [ 3, 57, 1197, 25137 ]
auto_complete_vals = [ 1, 2, 3, 4 ]

def validate_line(line: str) -> Tuple[bool, int]:
    input_queue = []
    for c in line:
        if c in open_chars:
            input_queue.append(c)
        else:
            open_char = input_queue.pop()
            if close_chars.index(c) != open_chars.index(open_char):
                return False, error_vals[close_chars.index(c)]

    # when we get to here, we need to insert all of the close
    # delimiters that are left in the left
    closing_chars = []
    for c in input_queue:
        closing_chars.insert(0, close_chars[open_chars.index(c)])

    total = 0
    for c in closing_chars:
        total = (total * 5) + auto_complete_vals[close_chars.index(c)]

    return True, total 



if __name__ == '__main__': 
    error_value = 0
    auto_complete_scores = []
    for l in lines:
        valid, value = validate_line(l)
        if valid:
            auto_complete_scores.append(value)
        else:
            error_value += value

    auto_complete_scores.sort()
    print(error_value, auto_complete_scores[len(auto_complete_scores)//2])