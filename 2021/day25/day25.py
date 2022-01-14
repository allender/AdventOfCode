from typing import List

with open('input.txt') as f:
	grid = f.read().split()

width, height = len(grid[0]), len(grid)

num_turns = 0
while True:

	# east swimmers
	east_grid = []
	east_moved = False
	for l in grid:
		rollover = False
		if l[width - 1] == '>' and l[0] == '.':
			rollover = True
		new_line = l.replace('>.', '.>')
		if rollover == True:
			new_line = '>' + new_line[1:width - 1] + '.'
		
		if new_line != l:
			east_moved = True

		east_grid.append(new_line)

	# south swimmers.  Transpose grid here and we
	# can have the same logic as above
	south_grid = [ ''.join(i) for i in zip(*east_grid) ] 
	grid = []
	south_moved = False
	for l in south_grid:
		rollover = False
		if l[height - 1] == 'v' and l[0] == '.':
			rollover = True
		new_line = l.replace('v.', '.v')
		if rollover == True:
			new_line = 'v' + new_line[1:height - 1] + '.'

		if new_line != l:
			south_moved = True

		grid.append(new_line)

	# retranspost the grid
	grid = [ ''.join(i) for i in zip(*grid) ] 

	num_turns += 1
	if east_moved == False and south_moved == False:
		break


print(num_turns)

