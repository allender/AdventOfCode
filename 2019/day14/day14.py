# pylint: disable=missing-docstring, unused-import, mixed-indentation

import sys
import os
from collections import defaultdict

MAX = 1000000000000

def get_reactions(lines):
    reactions = { }
    for line in  lines:
        input, output = line.split(' => ')
        inputs = [ ]
        for item in input.split(','):
            amount, name = item.split()
            inputs.append((int(amount), name))

        output_amount, ouput_name = output.split()
        reactions[ouput_name] = (int(output_amount), inputs)

    return reactions

def calculate_amount(reactions, quantity):
    # dictionary to keep track of counts for each element
    element_counts = defaultdict(int)
    element_counts['FUEL'] = quantity
    while True:
        found_element = False
        for element, count in element_counts.items():
            if element != 'ORE' and count > 0:
                found_element = True
                break

        if found_element is False:
            break

        source_count, element_sources = reactions[element]
        output_count = (count + source_count - 1) // source_count
        element_counts[element] -= source_count * output_count
        for count, material in element_sources:
            element_counts[material] += output_count * count 

    return element_counts['ORE']

def find_max_fuel(reactions):
    # calculate how much ore for one fuel
    max_ore_amount = MAX // calculate_amount(reactions, 1)

    # iterate with new quantities until we reach the max.  Get
    # quantity or ore needed for average of min/max and converge
    # until we get max just above min
    min_ore_amount = 2 * max_ore_amount
    while max_ore_amount < min_ore_amount - 1:
        quantity = (max_ore_amount + min_ore_amount) // 2
        new_amount = calculate_amount(reactions, quantity)
        if new_amount < MAX:
            max_ore_amount = quantity
        elif new_amount > MAX:
            min_ore_amount = quantity

    return max_ore_amount

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        lines = f.read().splitlines()

    reactions = get_reactions( lines )
    print(calculate_amount(reactions, 1))
    print(find_max_fuel(reactions))