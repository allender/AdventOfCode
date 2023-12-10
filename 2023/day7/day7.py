from aocd.models import Puzzle

puzzle = Puzzle(2023, 7)

class Hand():
    cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2' ]
    cards_no_jokers = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2' ]
    card_set = cards
    use_jokers = False

    @staticmethod
    def use_jokers():
        Hand.card_set = Hand.cards_no_jokers
        Hand.card_set.append('J')
        Hand.use_jokers = True

    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid
        self.counts = self.find_counts(Hand.cards)
        self.counts_with_jokers = self.find_counts(Hand.cards_no_jokers)
        self.rank = self.find_rank(self.counts,  0)
        self.joker_rank = self.find_rank(self.counts_with_jokers, self.hand.count('J'))

    def find_counts(self, cards):
        counts = [0] * len(cards)
        for index, c in enumerate(cards):
            counts[index] += self.hand.count(c)
        return counts
    
    def find_rank(self, counts, jokers):
        singles = counts.count(1)
        pairs = counts.count(2)
        threes = counts.count(3)
        fours = counts.count(4)
        fives = counts.count(5)

        rank = -1
        if singles == 5:
            rank = 0
        elif pairs == 1 and singles == 3:
            rank = 1
        elif pairs == 2 and singles == 1:
            rank = 2
        elif threes == 1 and singles == 2:
            rank = 3
        elif threes == 1 and pairs == 1:
            rank = 4
        elif fours == 1:
            rank = 5
        elif fives == 1:
            rank = 6

        if jokers == 0:
            return rank

        # four jokers gives five of a kind
        if jokers == 4 or jokers == 5:
            rank = 6

        # three jokers give four of a kind or five of a kind
        elif jokers == 3 and pairs == 0:
            rank = 5
        elif jokers == 3 and pairs == 1:
            rank = 6

        # two jokers might give full hour or three of a kind or 5 of a kind
        elif jokers == 2 and threes == 1:
            rank = 6
        elif jokers == 2 and pairs == 1:
            rank = 5
        elif jokers == 2 and pairs == 0:
            rank = 3

        # one jokers couild give a pair, three of a kind, ful hour, four or five of a kind
        elif jokers == 1 and singles == 4:
            rank = 1
        elif jokers == 1 and pairs == 1:
            rank = 3
        elif jokers == 1 and pairs == 2:
            rank = 4
        elif jokers == 1 and threes == 1:
            rank = 5
        elif jokers == 1 and fours == 1:
            rank = 6

        return rank

    def __lt__(self, other):
        if Hand.use_jokers == False:
            self_rank = self.rank
            other_rank = other.rank
        else:
            self_rank = self.joker_rank
            other_rank = other.joker_rank

        if self_rank < other_rank:
            return True
        
        # if ranks are the same, then compare each card
        if self_rank == other_rank:
            for c1, c2 in zip(self.hand, other.hand):
                if Hand.card_set.index(c1) > Hand.card_set.index(c2):
                    return True
                elif Hand.card_set.index(c1) < Hand.card_set.index(c2):
                    return False

        return False
    
    def __repr__(self):
        if Hand.use_jokers == False:
            return self.hand + ' ' + str(self.rank)
        else:
            return self.hand + ' ' + str(self.rank) + ' ' + str(self.joker_rank)

input = puzzle.input_data.splitlines()
# input = puzzle.examples[0][0].splitlines()

hands = [ Hand(parts[0], int(parts[1])) for i in input if (parts := i.split()) is not None ]

sorted_hands = sorted(hands)
total = sum( [ (rank + 1) * h.bid for rank,h in enumerate(sorted_hands) ] )
print(total)

Hand.use_jokers()
sorted_hands = sorted(hands)
total = sum( [ (rank + 1) * h.bid for rank,h in enumerate(sorted_hands) ] )
print(total)