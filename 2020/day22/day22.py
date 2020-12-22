import re
import queue

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

    while deck1.empty() == False and deck2.empty() == False:
        card1 = deck1.get()
        card2 = deck2.get()
        if card1 > card2:
            deck1.put(card1)
            deck1.put(card2)
        elif card2 > card1:
            deck2.put(card2)
            deck2.put(card1)
        else:
            assert("cards are equal")

        round += 1

Game_number = 1

def play_game_part2(deck1, deck2):
    round = 1
    global Game_number
    current_game = Game_number

    prev_hands = {}

    while deck1.empty() == False and deck2.empty() == False:
        # have we seen a hand before?  player 1 wins
        cards = (tuple(deck1.queue), tuple(deck2.queue))
        if cards in prev_hands:
            # to make player 1 win - so empty player 2's deck
            while deck2.empty() == False:
                deck2.get()

            return

        # keep track of previous decks
        prev_hands[cards] = 1

        # get cards
        card1 = deck1.get()
        card2 = deck2.get()

        # need to determine what to do based on rules of recursive.  Each
        # player must have at least as many cards as what he drew
        if len(deck1.queue) >= card1 and len(deck2.queue) >= card2:
            new_deck1 = queue.Queue()
            new_deck2 = queue.Queue()
            for idx in range(card1):
                new_deck1.put(deck1.queue[idx])
            for idx in range(card2):
                new_deck2.put(deck2.queue[idx])
            Game_number += 1
            play_game_part2(new_deck1, new_deck2)
            if len(new_deck2.queue) == 0:
                deck1.put(card1)
                deck1.put(card2)
            else:
                deck2.put(card2)
                deck2.put(card1)
        else:
            if card1 > card2:
                deck1.put(card1)
                deck1.put(card2)
            elif card2 > card1:
                deck2.put(card2)
                deck2.put(card1)
            else:
                assert("cards are equal")

        round += 1

    assert(len(deck1.queue) == 0 or len(deck2.queue) == 0)


if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')

    deck1 = queue.Queue()
    deck2 = queue.Queue()

    index = 1
    while data[index] != '':
        deck1.put(int(data[index]))
        index += 1

    index += 2
    while data[index] != '':
        deck2.put(int(data[index]))
        index += 1

    # play_game_part1(deck1, deck2)
    play_game_part1(deck1, deck2)
    deck1_list = list(deck1.queue)
    deck2_list = list(deck2.queue)

    score1 = sum( [ (len(deck1_list) - i) * val for i, val in enumerate(deck1_list) ] ) 
    score2 = sum( [ (len(deck2_list) - i) * val for i, val in enumerate(deck2_list) ] ) 

    print(score1, score2)

    # reinitialize everything
    deck1 = queue.Queue()
    deck2 = queue.Queue()

    index = 1
    while data[index] != '':
        deck1.put(int(data[index]))
        index += 1

    index += 2
    while data[index] != '':
        deck2.put(int(data[index]))
        index += 1

    play_game_part2(deck1, deck2)

    deck1_list = list(deck1.queue)
    deck2_list = list(deck2.queue)

    score1 = sum( [ (len(deck1_list) - i) * val for i, val in enumerate(deck1_list) ] ) 
    score2 = sum( [ (len(deck2_list) - i) * val for i, val in enumerate(deck2_list) ] ) 

    print(score1, score2)


