# pylint: disable=missing-docstring, unused-import, mixed-indentation

import os
import sys
import collections

def new_deck():
    return [ i for i in range(0, deck_size) ]

#part 1 by tracking the card

instructions = [ ]
for line in open('input.txt').readlines():
    instructions.append(line.rstrip('\n'))

pos = 2019
deck_size = 10007
deck = new_deck()
for instruction in instructions:
    if instruction == 'deal into new stack':
        pos = deck_size - 1 - pos

    elif instruction.startswith('deal with increment '):
        increment = int(instruction[instruction.rfind(' ')+1:])
        pos = (pos * increment) % deck_size

    elif instruction.startswith('cut '):
        cut_amount = int(instruction[instruction.rfind(' ')+1:])
        pos = (pos - cut_amount) % deck_size

print (pos)


# part 2
# need to track the instructions in reverse to figure out
# where the card in position 2020 started.  

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd( a, m )
    assert g != -1
    return x % m

def modpow(a, b, m, n):
    if m == 0:
        return 1, 0
    elif m % 2 == 0:
        return modpow( a * a % n, (a*b+b)%n, m // 2, n)
    else:
        c, d = modpow(a, b, m -1, n)
        return a * c % n, (a * d + b) % n

instructions = [ ]
for line in open('input.txt').readlines():
    instructions.append(line.rstrip('\n'))

pos =  2020
deck_size = 119315717514047
iterations = 101741582076661
a, b = 1, 0
for instruction in reversed(instructions):
    if instruction == 'deal into new stack':
        a = -a
        b = -b + deck_size -1

    elif instruction.startswith('deal with increment '):
        increment = int(instruction[instruction.rfind(' ')+1:])
        increment_inv = modinv(increment, deck_size)
        a = a * increment_inv % deck_size
        b = b * increment_inv % deck_size

    elif instruction.startswith('cut '):
        cut_amount = int(instruction[instruction.rfind(' ')+1:])
        b = (b + cut_amount) % deck_size

a, b = modpow(a, b, iterations, deck_size)
print((pos * a + b) % deck_size)