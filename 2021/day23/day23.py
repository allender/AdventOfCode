from aocd import lines
import re
from queue import PriorityQueue
import functools

test_lines = [
	'#############',
	'#...........#',
	'###B#C#B#D###',
	'  #A#D#C#A#',
	'  #########',
]

NUM_ROOMS = 4

PART2_LINES = [
	'  #D#C#B#A#',
	'  #D#B#A#C#'
]

# class to store information about a room
class Room():

	def __init__(self, amphipod, contents):
		self.amphipod = chr(ord('A') + amphipod)
		self.size = len(contents)
		self.contents = contents

	def __repr__(self):
		return f'{self.contents}'

	def remove_first(self):
		idx, val = [ (idx, x) for idx, x in enumerate(self.contents) if x is not None][0]
		self.contents[idx] = None
		return idx, val

	def set_first(self, value):
		for i in range(len(self.contents) - 1, -1, -1):
			if self.contents[i] == None:
				self.contents[i] = value
				return i

	def ready(self) -> bool:
		return all( [ x in (None, self.amphipod) for x in self.contents ] )

	def is_complete(self) -> bool:
		return all( [ x == self.amphipod for x in self.contents ] )

# class to hold Board state data
class Board():
	hallway_paths = None
	amphipod_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

	def __init__(self, hallway = None, rooms = None, score = 0):
		self.hallway = hallway
		self.rooms = rooms
		self.score = score 
		self.hash = None

		# create the hallway paths if they have not been created yet.  this
		# is mapping that gives the path of hallway locations from a room.  For
		# exampple, room 0 can go to space 0 in the hallway by touching space 1
		# and then space 0 in the hallway.  The hallway is just 7 locations - we don't
		# include the space above the rooms since we can't move to those locations.
		# therefore the hallways looks like this:
		#  01234567990
		#  xx.x.x.x.xx
		#    A B C D 
		#    A B C D
		#
		#  therefore the map is the cost of moving from room 0-3 to the given spot in the hallway
		if Board.hallway_paths is None:
			Board.hallway_paths = [ [ [ x for x in range(min(h, (l+1)*2), max(h, (l+1)*2) + 1) ] for l in range(4)] for h in range(11) ] 
			for r in range(NUM_ROOMS):
				for i in range(NUM_ROOMS):
					Board.hallway_paths[(i+1)*2][r] = None

	def __repr__(self):
		return f'{self.hallway} {self.rooms}'

	def __lt__(self, other):
		return self.score < other.score

	def __eq__(self, other):
		return self.hash == other.hash

	def __hash__(self):
		if self.hash is None:	
			h = []
			h.extend(self.hallway)
			h.extend( [y for x in self.rooms for y in x.contents])
			self.hash = hash(tuple(h))

		return self.hash

	# setups up the initial room configuration from the input
	# data, placing amphipods into the right room
	def setup(self, lines: list, part1: bool):
		room_lines = [ l for l in lines if 'A' in l or 'B' in l or 'C' in l or 'D' in l]
		if part1 == False:
			for i, l in enumerate(PART2_LINES):
				room_lines.insert(i+1, l)

		amphipods = re.findall('[ABCD]', ''.join(room_lines))
		room_size = len(room_lines)
		num_rooms = len(amphipods) // room_size 
		room_contents = [ [ amphipods[a] for a in range(i, len(amphipods), num_rooms) ] for i in range(num_rooms) ]
		self.rooms = [ Room(i, room_contents[i]) for i in range(num_rooms) ]
		self.hallway = [ None ] * 11

	# board is considered won if all of the amphipods
	# are in their proper room
	def won(self):
		return all([ r.is_complete() for r in self.rooms] )

	# do a move from a room to the hallway.  Makes a new # board
	def move_from_room(self, room: Room, hallpos: int):
		# create new hallway and rooms for the new board
		room_number = self.rooms.index(room)
		new_hallway = [ x for x in self.hallway ]
		new_rooms = [ Room(i, [x for x in self.rooms[i].contents]) for i,_ in enumerate(self.rooms) ]

		room_pos, new_hallway[hallpos] = new_rooms[room_number].remove_first()
		new_score = self.score + (len(Board.hallway_paths[hallpos][room_number]) + room_pos) * Board.amphipod_cost[new_hallway[hallpos]]

		# return the move
		return Board(new_hallway, new_rooms, new_score)

	def move_to_room(self, hallpos: int, room: Room):
		# create new hallway and rooms for the new board
		room_number = self.rooms.index(room)
		new_hallway = [ x for x in self.hallway ]
		new_rooms = [ Room(i, [x for x in self.rooms[i].contents]) for i,_ in enumerate(self.rooms) ]

		room_pos = new_rooms[room_number].set_first(self.hallway[hallpos])
		new_score = self.score + (len(Board.hallway_paths[hallpos][room_number]) + room_pos) * Board.amphipod_cost[new_hallway[hallpos]]
		new_hallway[hallpos] = None

		# return the move
		return Board(new_hallway, new_rooms, new_score)

	# returns true if a path is clear from the room
	# to the given hallway position
	def path_clear(self, room_number, hallway_location):
		path = Board.hallway_paths[hallway_location][room_number]
		if path is None:
			return False

		for p in path:
			if p != hallway_location and self.hallway[p] is not None:
				return False
		return True

	def generate_moves(self):
		moves = [ ]

		# generaste moves from hallway to rooms
		for hloc, h in enumerate(self.hallway):
			if h is not None:
				room_number = ord(h) - ord('A')
				if self.rooms[room_number].ready() == True and self.path_clear(room_number, hloc):
					new_board = self.move_to_room(hloc, self.rooms[room_number])
					moves.append(new_board)

		# generate moves from the rooms to the hallways
		for index, room in enumerate(self.rooms):
			# room ready to receive only
			if room.ready() == True:
				continue

			for hloc, h in enumerate(self.hallway):
				if h is None and self.path_clear(index, hloc):
					new_board = self.move_from_room(room, hloc)
					moves.append(new_board)

		return moves

def part1(starting_board: Board) -> int:
	# set priority queuea
	q = PriorityQueue()
	visited = set()

	q.put(starting_board)
	while q.empty() == False:
		board = q.get()
		if board.won() == True:
			return board
		elif board not in visited:
			visited.add(board)
			for new_board in board.generate_moves():
				q.put(new_board)

	return -1 

if __name__ == '__main__':
	board = Board()
	board.setup(lines, False)
	part1_board = part1(board)
	print(part1_board.score)

# from aocd import lines
# from copy import deepcopy
# from itertools import count
# import re
# from queue import PriorityQueue
# from typing import Counter, List, Tuple

# NUM_ROOMS = 4
# HALLWAY_LENGTH = 11
# AMPIPOD_TYPES = [ 'A', 'B', 'C', 'D' ]
# AMPHIPOD_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
# Counter = count()

# HALLWAY_PATHS = [ [ [ x for x in range(min(h, (l+1)*2), max(h, (l+1)*2) + 1) ] for l in range(NUM_ROOMS)] for h in range(HALLWAY_LENGTH) ] 
# for r in range(NUM_ROOMS):
# 	for i in range(NUM_ROOMS):
# 		HALLWAY_PATHS[(i+1)*2][r] = None

# def state_hash(burrow: dict) -> int:
# 	h = []
# 	h.extend(burrow['h'])
# 	h.extend( [x for a in AMPIPOD_TYPES for x in burrow[a]] )
# 	return hash(tuple(h))

# def board_setup(lines: List[str], part1 = True) -> Tuple:
# 	if part1 == False:
# 		lines = lines[2:3] + PART2_LINES + lines[3:4]

# 	amphipods = re.findall('[ABCD]', ''.join(lines))
# 	state = {}
# 	state['h'] = [ None ] * HALLWAY_LENGTH
# 	state['A'] = [ x for i in range (0, len(amphipods), 4) for x in amphipods[i] ]
# 	state['B'] = [ x for i in range (1, len(amphipods), 4) for x in amphipods[i] ]
# 	state['C'] = [ x for i in range (2, len(amphipods), 4) for x in amphipods[i] ]
# 	state['D'] = [ x for i in range (3, len(amphipods), 4) for x in amphipods[i] ]
# 	return (0, next(Counter), state, state_hash(state))

# def room_ready(state: Tuple, amphipod: chr) -> bool:
# 	return all( [ x in (None, amphipod) for x in state[amphipod] ] )

# def path_clear(state: Tuple, room: chr, hloc: int) -> bool:
# 	path = HALLWAY_PATHS[hloc][ord(room) - ord('A')]
# 	if path is None:
# 		return False

# 	for p in path:
# 		if p != hloc and state['h'][p] is not None:
# 			return False

# 	return True

# def move_to_room(burrow: dict, room: chr, hloc: int, cur_score: int) -> Tuple:
# 	new_burrow = deepcopy(burrow)
# 	for room_pos in range(len(new_burrow[room]) - 1, -1, -1):
# 		if new_burrow[room][room_pos] == None:
# 			break

# 	new_burrow[room][room_pos] = room
# 	new_burrow['h'][hloc] = None
# 	new_score = (len(HALLWAY_PATHS[hloc][ord(room) - ord('A')]) + room_pos) * AMPHIPOD_COST[room]
# 	return (cur_score + new_score, next(Counter), new_burrow, state_hash(new_burrow))

# def move_from_room(burrow: dict, room: chr, hloc: int, cur_score: int) -> Tuple:
# 	new_burrow = deepcopy(burrow)
# 	for room_pos in range(0, len(new_burrow[room])):
# 		if new_burrow[room][room_pos] != None:
# 			break

# 	new_burrow['h'][hloc] = new_burrow[room][room_pos]
# 	new_burrow[room][room_pos] = None
# 	new_score = (len(HALLWAY_PATHS[hloc][ord(room) - ord('A')]) + room_pos) * AMPHIPOD_COST[new_burrow['h'][hloc]]
# 	return (cur_score + new_score, next(Counter), new_burrow, state_hash(new_burrow))

# def generate_moves(burrow: dict, cur_score: int) -> List[Tuple]:
# 	moves = []

# 	# generaste moves from hallway to rooms
# 	for hloc, a in enumerate(burrow['h']):
# 		if a is not None:
# 			if room_ready(burrow, a) == True and path_clear(burrow, a, hloc):
# 				new_state = move_to_room(burrow, a, hloc, cur_score)
# 				moves.append(new_state)

# 	# generate moves from the rooms to the hallways
# 	for room in AMPIPOD_TYPES:
# 		if room_ready(burrow, room) == True:
# 			continue

# 		for hloc, h in enumerate(burrow['h']):
# 			if h is None and path_clear(burrow, room, hloc):
# 				new_board = move_from_room(burrow, room, hloc, cur_score)
# 				moves.append(new_board)

# 	return moves

# def won(state: dict) -> bool:
# 	for a in AMPIPOD_TYPES:
# 		if any( [ x != a for x in state[a] ]):
# 			return False

# 	return True

# def solve(starting_state: Tuple) -> Tuple:
# 	q = PriorityQueue()
# 	visited = set()

# 	q.put(starting_state)

# 	while q.empty() == False:
# 		state = q.get()
# 		if won(state[2]) == True:
# 			return state	 
		
# 		# mark this as visited
# 		if state[3] not in visited:
# 			visited.add(state[3])
# 			for new_state in generate_moves(state[2], state[0]):
# 				q.put(new_state)

# 	return (-1, None)

# if __name__ == '__main__':
# 	board = board_setup(lines, False)
# 	print(solve(board)[0])
# 	board = board_setup(lines, True)
# 	print(solve(board)[0])
