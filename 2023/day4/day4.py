from aocd.models import Puzzle

puzzle = Puzzle(2023, 4)
lines = puzzle.input_data.splitlines()
# lines = puzzle.examples[0][0].splitlines()

class Card():
    def __init__(self, data):
        _,numbers = data.split(':')
        winning_numbers, card_numbers = numbers.split('|')
        self.num_copies = 1
        self.winning_numbers = winning_numbers.split()
        self.card_numbers = card_numbers.split()

        self.num_winning_numbers = len(set(self.winning_numbers) & set(self.card_numbers))
        self.card_score = self.calculate_score()

    def calculate_score(self):
        if self.num_winning_numbers > 0:
            return 2 ** (self.num_winning_numbers - 1)

        return 0
    
    def add_copy(self, num_copies_to_add):
        self.num_copies += num_copies_to_add 
    
all_cards = []
for l in lines:    
    card = Card(l)
    all_cards.append(card)

print(sum([ x.card_score for x in all_cards ]))

for index, c in enumerate(all_cards):
    for number in range(c.num_winning_numbers):
        all_cards[index + number + 1].add_copy(c.num_copies)

print(sum ([ x.num_copies for x in all_cards ] ))
