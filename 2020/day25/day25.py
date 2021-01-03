from functools import reduce
from collections import Counter
from collections import defaultdict

test_data = """5764801
17807724"""

def find_loop(subject_num, key):
    loop = 1
    while True:
        if key == pow(subject_num, loop, 20201227):
            break
        loop += 1
    return loop

if __name__ == "__main__":
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')
    card_public = int(data[0])
    door_public = int(data[1])
    print(card_public, door_public)

    card_loop = find_loop(7, card_public)
    door_loop = find_loop(7, door_public)

    print(pow(door_public, card_loop, 20201227))