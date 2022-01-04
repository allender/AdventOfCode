from aocd import lines
from dataclasses import dataclass
from typing import Tuple
from itertools import product, cycle
import functools

test_lines = [
	'Player 1 starting position: 4',
	'Player 2 starting position: 8'
]

class Deterministic_Die():
	def __init__(self):
		self.cycler = cycle(range(1, 101))
		self.total_rolls = 0

	def roll(self):
		self.total_rolls += 3
		return [ next(self.cycler) for _ in range(3) ]

class Quantum_Die():
	def __init__(self):
		self.rolls = product((1, 2, 3), repeat=3)

def move(space, rolls: list):
	space = space + sum([x for x in rolls]) 
	while space > 10:
		space -= 10
	return space

def parse_input(lines: list):
	p1_start = int(lines[0].split(':')[1])
	p2_start = int(lines[1].split(':')[1])
	return p1_start, p2_start

def do_game(player1_space, player2_space, die):
	player1_score = 0
	player2_score = 0

	while True:
		player1_space = move(player1_space, die.roll())
		player1_score += player1_space
		if player1_score >= 1000:
			return player1_score, player2_score

		player2_space = move(player2_space, die.roll())
		player2_score += player2_space
		if player2_score >= 1000:
			return player1_score, player2_score

def part1(player1_start, player2_start):
	die = Deterministic_Die()
	scores = do_game(player1_start, player2_start, die)
	return die.total_rolls * min(scores)

@functools.lru_cache(None)
def do_universes(player1_space, player1_score, player2_space, player2_score):
	p1_wins = 0
	p2_wins = 0
	die = Quantum_Die()
	for roll in die.rolls:
		new_player1_space = move(player1_space, roll)
		new_player1_score = player1_score + new_player1_space
		if new_player1_score >= 21:
			p1_wins += 1
		else:
			new_wins_2, new_wins_1 = do_universes(player2_space, player2_score, new_player1_space, new_player1_score)
			p1_wins += new_wins_1
			p2_wins += new_wins_2

	return p1_wins, p2_wins

def part2(player1_start, player2_start):
	wins = do_universes(player1_start, 0, player2_start, 0)
	return wins
		
if __name__ == '__main__':
	player1_start, player2_start = parse_input(lines)
	print(part1(player1_start, player2_start))
	print(part2(player1_start, player2_start))
