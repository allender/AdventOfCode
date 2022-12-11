from aocd.models import Puzzle

puzzle = Puzzle(year=2022, day = 11)

class Monkey():
    all_monkeys = []
    group_mult = 1

    @classmethod
    def clear(cls):
        cls.group_mult = 1
        cls.all_monkeys = []

    @classmethod
    def print_result(cls):
         totals = sorted([ x.inspection_count for x in cls.all_monkeys ])
         print(totals[-1] * totals[-2])

    @classmethod
    def do_round(cls, part1 = True):
        for monkey in cls.all_monkeys:
            while monkey.items:
                monkey.inspection_count += 1
                new = int(eval(monkey.operation.format(old = monkey.items.pop(0))))
                if part1 == True:
                    new = new // 3
                else:
                    new = new % cls.group_mult
                if new % monkey.test == 0:
                    cls.all_monkeys[monkey.true_monkey].items.append(new)
                else:
                    cls.all_monkeys[monkey.false_monkey].items.append(new)

    def __init__(self, lines):
        Monkey.all_monkeys.append(self)
        self.id = len(self.all_monkeys) - 1
        self.items = [ x for x in map(int, lines[0].strip().split(':')[1].split(',')) ]
        self.inspection_count = 0
        self.operation = lines[1].split('=')[1].strip().replace('old', '{old}')
        self.test = int(lines[2].split()[3])
        Monkey.group_mult = self.group_mult * self.test
        self.true_monkey = int(lines[3].split()[5])
        self.false_monkey = int(lines[4].split()[5])


data = puzzle.input_data.splitlines()
for index in range(0, len(data), 7):
    monkey = Monkey(data[index + 1: index + 6])
for _ in range(20):
    Monkey.do_round(True)
Monkey.print_result()

Monkey.clear()
for index in range(0, len(data), 7):
    monkey = Monkey(data[index + 1: index + 6])

for _ in range(10000):
    Monkey.do_round(False)
Monkey.print_result()


