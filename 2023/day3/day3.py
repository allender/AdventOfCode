from aocd.models import Puzzle
import re

puzzle = Puzzle(2023, 3)
lines = puzzle.input_data.splitlines()
# lines = puzzle.examples[0][0].splitlines()

class Engine():
    symbol_re = re.compile(r'(?!\d|\.).')
    part_re = re.compile(r'(\d+)')
    gear_re = re.compile(r'\*')

    def __init__(self, input):
        self.schematic = input
        self.schematic_width = len(input[0])
        self.schematic_height = len(input)

    def get_part_number(self, index, gear_x):
        if index < 0 or index == self.schematic_height:
            return []

        part_numbers = []    
        for m in self.part_re.finditer(self.schematic[index]):
            if m.start(0) in range(gear_x -1, gear_x + 2) or m.end(0) - 1 in range(gear_x - 1, gear_x + 2):
                part_numbers.append(int(m.group(0)))

        return part_numbers
    
    def find_all_parts(self):
        parts_total = 0
        for index, _ in enumerate(self.schematic):
            part_numbers = []
            for m in self.symbol_re.finditer(self.schematic[index]):
                part_numbers.extend([ self.get_part_number(index + x, m.start(0)) for x in [-1, 0, 1] ]) 

            part_numbers = [ pn for x in part_numbers for pn in x if x] 
            parts_total += sum(part_numbers)

        print(parts_total)

    def find_gear_ratios(self):
        gear_ratio = 0
        for index, _ in enumerate(self.schematic):
            for m in self.gear_re.finditer(self.schematic[index]):
                part_numbers = [ self.get_part_number(index + x, m.start(0)) for x in [-1, 0, 1] ] 
                part_numbers = [ pn for x in part_numbers for pn in x if x] 
                if len(part_numbers) == 2:
                    gear_ratio += part_numbers[0] * part_numbers[1]

        print(gear_ratio)
            
    
engine = Engine(lines)
engine.find_all_parts()
engine.find_gear_ratios()
