import re
import queue
import time
import sys

test_data="""Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""

def play_game_part1(deck1, deck2):
    round = 1

    while len(deck1) > 0 and len(deck2) > 0:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        elif card2 > card1:
            deck2.append(card2)
            deck2.append(card1)
        else:
            assert("cards are equal")

        round += 1

def play_game_part2(deck1, deck2, level):
    round = 1
    prev_hands = {}

    while len(deck1) > 0 and len(deck2) > 0:
        # optimization if we are in recursion (i.e. a sub game), can
        # we declare the winner just by looking at the cards?
        if level > 0:
            max1 = max(deck1)
            max2 = max(deck2)
            if max1 > max2:
                return (deck1, [])

        # have we seen a hand before?  player 1 wins
        cards = (tuple(deck1), tuple(deck2))
        if cards in prev_hands:
            deck2 = []
            return (deck1, [])

        # keep track of previous decks
        prev_hands[cards] = 1

        # get cards
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)

        # need to determine what to do based on rules of recursive.  Each
        # player must have at least as many cards as what he drew
        if len(deck1) >= card1 and len(deck2) >= card2:
            d1, d2 = play_game_part2(deck1[:card1], deck2[:card2], level + 1)
            if len(d2) == 0:
                deck1.extend([card1, card2])
            else:
                deck2.extend([card2, card1])
        else:
            if card1 > card2:
                deck1.extend([card1, card2])
            elif card2 > card1:
                deck2.extend([card2, card1])

        round += 1

    return (deck1, deck2)


if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')

    deck1 = []
    deck2 = []

    index = 1
    while data[index] != '':
        deck1.append(int(data[index]))
        index += 1

    index += 2
    while data[index] != '':
        deck2.append(int(data[index]))
        index += 1

    # play_game_part1(deck1, deck2)
    play_game_part1(deck1, deck2)

    score1 = sum( [ (len(deck1) - i) * val for i, val in enumerate(deck1) ] ) 
    score2 = sum( [ (len(deck2) - i) * val for i, val in enumerate(deck2) ] ) 

    print(score1, score2)

    # reinitialize everything
    deck1 = []
    deck2 = []

    index = 1
    while data[index] != '':
        deck1.append(int(data[index]))
        index += 1

    index += 2
    while data[index] != '':
        deck2.append(int(data[index]))
        index += 1

    start = time.time()
    deck1, deck2 = play_game_part2(deck1, deck2, 0)
    end = time.time()
    print(end - start)

    score1 = sum( [ (len(deck1) - i) * val for i, val in enumerate(deck1) ] ) 
    score2 = sum( [ (len(deck2) - i) * val for i, val in enumerate(deck2) ] ) 

    print(score1, score2)


