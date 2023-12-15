from aocd.models import Puzzle
import re

puzzle = Puzzle(2023, 15)

inputs = puzzle.input_data.strip().split(',')
# inputs = puzzle.examples[0][0].strip().split(',')

def find_hash(s):
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value

def part1():
    return sum(find_hash(s) for s in inputs) 

def part2():
    boxes = {}
    for s in inputs:
        parts = re.split(r'-|=', s)
        lens_label = parts[0]
        box = find_hash(lens_label)

        # create a new entry if we don't have one
        if box not in boxes:
            boxes[box] = ([],[])
        
        if parts[1]:
            new_lens_number = int(parts[1])
            if lens_label in boxes[box][0]:
                index = boxes[box][0].index(lens_label)
                boxes[box][1][index] = new_lens_number
            else:
                boxes[box][0].append(lens_label)
                boxes[box][1].append(new_lens_number)

        else:
            if lens_label in boxes[box][0]:
                index = boxes[box][0].index(lens_label)
                boxes[box][0].pop(index)
                boxes[box][1].pop(index)

    return sum((box_num + 1) * (index + 1) * lens for box_num, parts in boxes.items() for index, lens in enumerate(parts[1])) 


print(part1())
print(part2())