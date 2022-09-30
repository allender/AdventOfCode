from collections import namedtuple
from typing import List, Tuple

ALU = namedtuple('ALU', ['x', 'y', 'z', 'w'])

test_lines = [
	'inp x'
]

binary_lines = [
	'inp w',
	'add z w',
	'mod z 2',
	'div w 2',
	'add y w',
	'mod y 2',
	'div w 2',
	'add x w',
	'mod x 2',
	'div w 2',
	'mod w 2',
]

class ALU():
	register_names = ('x', 'y', 'z', 'w')

	def __init__(self, input_func):
		self.register = dict.fromkeys(ALU.register_names, 0)
		self.input_func = input_func()

	def __str__(self):
		return f'{self.register}'

	def run_program(self, lines: List[str]):
		for l in lines:
			try:
				op, r1, r2 = l.split(' ')
			except ValueError:
				op, r1 = l.split(' ')
				r2 = None

			val = 0
			if r2:
				if r2 in ALU.register_names:
					val = self.register[r2]
				else:
					val = int(r2)

			if op == 'inp':
				print(self)
				self.register[r1] = next(self.input_func)
			elif op == 'add':
				self.register[r1] = self.register[r1] + val
			elif op == 'mul':
				self.register[r1] = self.register[r1] * val
			elif op == 'div':
				self.register[r1] = self.register[r1] // val
			elif op == 'mod':
				self.register[r1] = self.register[r1] % val
			elif op == 'eql':
				if self.register[r1] - val == 0:
					self.register[r1] = 1
				else:
					self.register[r1] = 0
			else:
				assert False

def input_func():
	number = '11111111111111'
	for i in number:
		yield int(i)

def read_program(lines: List[str]) -> Tuple:
	x_adds = []
	y_adds = []
	for i in range(14):
		x_adds.append(int(lines[(i*18) + 5][6:]))
		y_adds.append(int(lines[(i*18) + 15][6:]))

	return x_adds, y_adds

def digit_calc(alu: ALU, div26: bool, add_x: int, add_y: int):
	if div26 == True:
		alu.register['z'] = alu.register['z'] // 26

	if (alu.register['z'] % 26) + add_x == alu.register['w']:
		alu.register['x'] = 0
		alu.register['y'] = 0
	else:
		alu.register['z'] = (alu.register['z'] * 26)
		alu.register['y'] = add_y + alu.register['w']
		alu.register['z'] += alu.register['y']

if __name__ == '__main__':
	with open('input.txt') as f:
		lines = f.read().splitlines()

	x_adds, y_adds = read_program(lines)
	alu = ALU(input_func)
	alu.run_program(lines)
	print(alu)
