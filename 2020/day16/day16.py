import re
import time
from collections import namedtuple

test_data = """class: 1-3 or 5-7
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

    @classmethod
    def add_item(cls, name, low0, high0, low1, high1):
        cls.ticket_items[name] = ((low0, high0, low1, high1))

    @classmethod
    def get_names(cls):
        return [ item for item in cls.ticket_items.keys() ]

    @classmethod
    def find_valid_fields(cls, valid_fields):
        cls.field_mappings = [None] * len(cls.ticket_items)
        index = 0
        while index < len(cls.ticket_items):
            cur_field = [ (i, x[0]) for i,x in enumerate(valid_fields) if len(x) == 1 ]
            assert( len(cur_field) == 1 )
            cur_field = cur_field[0]

            # we now know that a column matches a field name
            cls.field_mappings[cur_field[0]] = cur_field[1]
            for f in valid_fields:
                if cur_field[1] in f:
                    f.remove(cur_field[1])

            index += 1

        return

    def __init__(self, values):
        self.values =  values

    def invalid_for_any_field(self):
        result = list(self.values) 

        # loop over all values and see if values are valid for any field
        for val in self.values:
            for item in self.ticket_items.values():
                if (val >= item[0] and val <= item[1]) or (val >= item[2] and val <= item[3]):
                    result.remove(val)
                    break

        return result

    def get_invalid_fields(self):
        result = [ ]
        for val in self.values:
            names = [ n for n, item in self.ticket_items.items() if (val < item[0] or (val > item[1] and val < item[2]) or val > item[3]) ]
            result.append(names)
                    
        return result

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

    valid_names = [ ]
    for i in enumerate(Ticket.ticket_items):
        valid_names.append(ticket.get_names())

    for ticket in remaining_tickets:
        invalid_ticket_fields = ticket.get_invalid_fields()
        for index, fields in enumerate(invalid_ticket_fields):
            for f in fields:
                if f in valid_names[index]:
                    valid_names[index].remove(f)


    Ticket.find_valid_fields(valid_names)

    val = 1
    for i, f in enumerate(Ticket.field_mappings):
        if 'departure' in f:
            val *= my_ticket.values[i]  

    print(val)