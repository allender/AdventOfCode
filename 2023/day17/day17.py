from aocd.models import Puzzle
from collections import defaultdict
from dataclasses import dataclass, field
from queue import PriorityQueue
import math

puzzle = Puzzle(2023, 17)

inputs = puzzle.input_data.strip().split('\n')
# inputs = puzzle.examples[0][0].split('\n')

map = { complex(x, y): int(c) for y,l in enumerate(inputs) for x,c in enumerate(l) }

start = complex(0, 0)
end = complex(len(inputs[0]) - 1, len(inputs) - 1)

# dirs we can traval (in complex form).  N, S, E, W
dirs = [ -1, 1, 1j, -1j]

@dataclass(order=True)
class QueueNode:
    cost: int
    data: tuple=field(compare=False)

def find_path(min_steps, max_steps):
    node_queue = PriorityQueue()
    node_queue.put( QueueNode(0, (complex(0,0), 0)))  # first queue entry.  cost, x, y, cur_dir
    visited = set()          # which nodes we have been to
    costs = defaultdict(lambda: math.inf)               # lowest cost to get to the nodes

    while node_queue:
        node = node_queue.get()
        cost, data = node.cost, node.data
        cur_pos, cur_dir = data

        # is the x/y where we need to be, and if so, we are done
        if cur_pos == end:
            return cost
        
        if (cur_pos, cur_dir) in visited:
            continue

        visited.add((cur_pos, cur_dir))
        for new_dir in dirs:
            # at this point, we have moved max spaces in the current
            # direction and we can't go further, nor can we go back
            if new_dir == cur_dir or new_dir == -cur_dir:
                continue

            # move the maximum steps in the given direction
            # at which point we can't move that direction anymore
            increase = 0
            new_pos = cur_pos
            for cur_step in range(0, max_steps):
                new_pos += new_dir  
                # need to make sure new position is in the grid
                if 0 <= new_pos.real < len(inputs[0]) and 0 <= new_pos.imag < len(inputs):
                    increase += map[new_pos]
                    if cur_step < min_steps - 1:
                        continue
                    new_cost = cost + increase
                    if new_cost < costs[(new_pos, new_dir)]:
                        costs[(new_pos, new_dir)] = new_cost
                        node_queue.put( QueueNode(new_cost, (new_pos, new_dir)) )

print(find_path(1, 3))
print(find_path(4, 10))
