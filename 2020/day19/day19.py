import re 

test_data = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

rules = {}
tests = None

class Rule():
    def __init__(self, value):
        self.value = value
        if type(value) == list:
            self.solve = self.list_solver
        else:
            self.solve = self.character_solver

    def character_solver(self, test_string):
        if test_string and test_string.startswith(self.value):
            return set( [self.value] )
        return [] 

    def list_solver(self, test_string):
        if not test_string:
            return set() 

        all_strings = set() 
        for seq in self.value:
            strings_so_far = [''] 
            for rule_number in seq:
                strings_so_far = set( s + new_string for s in strings_so_far for new_string in rules[rule_number].solve(test_string[len(s):]) )

            all_strings = all_strings | strings_so_far

        return all_strings

if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')

    index = 0;
    while data[index] != '':
        mo = re.match( r'^(\d+): (?:"(.)"|(\d.*))', data[index])
        rule_number = int(mo.group(1))
        if mo.group(2) is not None:
            rules[rule_number] = Rule(mo.group(2))
        else:
            rule_matches = mo.group(3).split(' | ')
            rule_numbers = [ list(map(int, s.split(' '))) for s in rule_matches ]
            rules[rule_number]  = Rule(rule_numbers)

        index += 1

    tests = data[index + 1:]

    num_match = sum( [ 1 if test in rules[0].solve(test) else 0 for test in tests ] )
    print(num_match)

    rules[8] = Rule([ [42], [42, 8] ])
    rules[11] = Rule([ [42, 31], [42, 11, 31] ])
    num_match = sum( [ 1 if test in rules[0].solve(test) else 0 for test in tests ] )
    print(num_match)
