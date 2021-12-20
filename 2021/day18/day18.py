from aocd import lines
from typing import List
import math
from itertools import permutations
from copy import deepcopy

class Snail:
	def __init__(self, left = None, right = None, parent = None, value = None):
		self.left = left 
		self.right = right 
		self.parent = parent
		self.value = value

		if self.left is not None:
			self.left.parent = self
		if self.right is not None:
			self.right.parent = self

	def __str__(self):
		if self.value is not None:
			return str(self.value)
		else:
			return '[' + str(self.left) + ',' + str(self.right) + ']'

test_lines = [
	# '[[[[[9,8],1],2],3],4]',
	# '[7,[6,[5,[4,[3,2]]]]]',
	# '[[6,[5,[4,[3,2]]]],1]',
	# '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
	# '[[[[4,3],4],4],[7,[[8,4],9]]]',
	# '[1,1]'
	'[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
	'[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
	# '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
	# '[[[5,[2,8]],4],[5,[[9,9],0]]]',
	# '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
	# '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
	# '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
	# '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
	# '[[[[5,4],[7,7]],8],[[8,3],8]]',
	# '[[9,3],[[9,9],[6,[4,9]]]]',
	# '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
	# '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]',
]

def snail_to_explode(snail: Snail, depth = 0) -> Snail:
	if snail is None or snail.value is not None:
		return None

	if depth == 4:
		return snail

	exploded_snail = snail_to_explode(snail.left, depth + 1)
	if exploded_snail is not None:
		return exploded_snail

	exploded_snail = snail_to_explode(snail.right, depth + 1)
	if exploded_snail is not None: 
		return exploded_snail

	return None

def explode(snail: Snail):
	# if this is on the right side of the pair, look
	# left to find rightmost value to add to this node's value
	node = snail
	while True:
		if node.parent == None:
			break
		if node == node.parent.right:
			node = node.parent.left
			while node.right is not None:
				node = node.right
			node.value += snail.left.value
			break
		else:
			node = node.parent


	# otherwise look right to find the leftmost value
	# to add
	node = snail
	while True:
		if node.parent == None:
			break
		if node == node.parent.left:
			node = node.parent.right
			while node.left is not None:
				node = node.left
			node.value += snail.right.value
			break
		else:
			node = node.parent

	snail.left = None
	snail.right = None
	snail.value = 0

def snail_to_split(snail: Snail) -> Snail:
	if snail.value is not None:
		if snail.value >= 10:
			return snail
		else:
			return None

	split_snail = snail_to_split(snail.left)
	if split_snail is not None:
		return split_snail

	split_snail = snail_to_split(snail.right)
	if split_snail is not None: 
		return split_snail

	return None

# splitting is easy - just create a new node
# in this node's place with the values
# according to the puzzle
def split(snail: Snail):
	snail.left = Snail(None, None, snail, math.floor(snail.value / 2))
	snail.right = Snail(None, None, snail, math.ceil(snail.value / 2))
	snail.value = None

# explodes all of the parts of this snail
def parse_node(parent: Snail, data):
	if type(data) == list:
		parent.left = Snail(None, None, parent, None)
		parse_node(parent.left, data[0])
		parent.right = Snail(None, None, parent, None)
		parse_node(parent.right, data[1])

	elif type(data) == int:
		parent.value = data

def reduce_snail(snail: Snail):
	while True:
		to_explode = snail_to_explode(snail)
		if to_explode is not None:
			explode(to_explode)
			continue

		to_split = snail_to_split(snail)
		if to_split is not None:
			split(to_split)
			continue

		break

def parse_lines(lines: List[str]) -> List[Snail]:
	snails = []
	for l in lines:
		snail = Snail()
		parse_node(snail, eval(l))
		reduce_snail(snail)
		snails.append(snail)

	return snails

def magnitude(snail: Snail) -> int:
	if snail.value is not None:
		return snail.value
	
	return (3 * magnitude(snail.left)) + (2 * magnitude(snail.right))

def part1(snails: List[Snail]) -> int:
	snail_sum = snails[0]
	for s in snails[1:]:
		snail_sum = Snail(snail_sum, s, None, None)
		reduce_snail(snail_sum)

	return magnitude(snail_sum)

def part2(snails: List[Snail]) -> int:
	perms = permutations(snails, 2)
	biggest_mag = 0
	for x, y in list(perms):
		sum = Snail(deepcopy(x), deepcopy(y), None, None)
		reduce_snail(sum)
		new_magnitude = magnitude(sum)
		if new_magnitude > biggest_mag:
			biggest_mag = new_magnitude

	return biggest_mag

if __name__ == '__main__': 
	snails = parse_lines(lines)
	print(part1(snails))
	snails = parse_lines(lines)
	print(part2(snails))
