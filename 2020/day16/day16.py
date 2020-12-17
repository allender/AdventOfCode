import re
import time
import functools

part1_data = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

part2_data = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""

class Ticket():
    ticket_items = {} 
    field_mappings = []
    fields = []

    @classmethod
    def add_item(cls, name, low0, high0, low1, high1):
        cls.ticket_items[name] = (lambda n : (low0 <= n <= high0) or (low1 <= n <= high1))

    @classmethod
    def get_names(cls):
        return [ item for item in cls.ticket_items.keys() ]

    @classmethod
    def find_field_order(cls, possible):
        cls.fields = { }
        while possible:
            key, column = [ (key, sum(values) ) for key, values in possible.items() if len(values) == 1 ][0]
            cls.fields[key] = column
            possible = { key : [ v for v in values if v != column ] for key, values in possible.items() if len(values) != 1 }

    def __init__(self, values):
        self.values =  values

    def invalid_for_any_field(self):
        valid_values = [ x for name, cond in self.ticket_items.items() for x in self.values if cond(x) == True ]
        return [ v for v in self.values if v not in valid_values ]

    def get_invalid_fields(self):
        return [ [n for n, cond in self.ticket_items.items() if cond(val) == False] for val in self.values ]

if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')

    ticket_item_re = re.compile(r'(?P<name>[\w ]+): (?P<low1>\d+)\-(?P<high1>\d+) or (?P<low2>\d+)\-(?P<high2>\d+)')

    index = 0
    their_tickets = []
    while data[index] != '':
        ticket_mo = ticket_item_re.match(data[index]) 
        Ticket.add_item(ticket_mo.group('name'), int(ticket_mo.group('low1')),
            int(ticket_mo.group('high1')),
            int(ticket_mo.group('low2')),
            int(ticket_mo.group('high2')))
        index += 1

    index += 2
    ticket_values = list(map(int, data[index].split(',')))
    my_ticket = Ticket(ticket_values)

    index += 3
    while data[index] != '':
        ticket_values = list(map(int, data[index].split(',')))
        their_tickets.append(Ticket(ticket_values))
        index += 1

    s = 0
    remaining_tickets = []
    for ticket in their_tickets:
        l = ticket.invalid_for_any_field()
        if l:
            s += sum(ticket.invalid_for_any_field())
        else:
            remaining_tickets.append(ticket)

    print(s)

    possible = {}
    for f, cond in Ticket.ticket_items.items():
        possible[f] = [ x for x in range(len(my_ticket.values)) if all(map(lambda t: cond(t.values[x]), remaining_tickets)) ]

    # Ticket.find_valid_fields(valid_names)
    Ticket.find_field_order(possible)

    val = functools.reduce(lambda x, y: x * y, [ my_ticket.values[val] for key, val in Ticket.fields.items() if 'departure' in key ])
    print(val)