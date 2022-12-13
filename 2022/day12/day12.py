from aocd.models import Puzzle
from collections import deque, defaultdict

puzzle = Puzzle(year=2022, day = 12)

test_data = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''

class Graph():
    def __init__(self, heightmap: dict):
        self.nodes = heightmap

    def __repr__(self):
        return f'{self.x}, {self.y} -- {self.height}'

    # computes the neighbors making sure we don'tr run off the end of the grid
    def get_valid_neighbors(self, node):
        return [(node[0] + x, node[1] + y) for (x,y) in [(-1,0), (1,0), (0,-1), (0,1)] if (node[0] + x, node[1] + y) in self.nodes ]

    def bsf(self, starting_node, end_node, part2 = False):
        queue = deque()
        queue.append(starting_node)
        visited = set()
        visited.add(starting_node)

        # distances from start to given node
        distances = defaultdict(int)
        
        while queue:
            current = queue.popleft()
            if part2 == False and current == end_node:
                return distances[current]

            # for part 2 just need to find the first 'a'
            if part2 == True and self.nodes[current] == ord('a'):
                return distances[current]

            # note that we are going from end to start (for both parts) so the logic here
            # to determine valid neighbor is reversed from the description
            for n in self.get_valid_neighbors(current):
                if n not in visited and (self.nodes[n] >= self.nodes[current] - 1):
                    queue.append(n)
                    visited.add(n)
                    distances[n] = distances[current] + 1

        return -1


data = puzzle.input_data
start_node = None
end_node = None
heightmap = {}
for y, l in enumerate(data.splitlines()):
    for x, h in enumerate(l):
        if h == 'S':
            start_node = (x,y)
            h = 'a'
        elif h == 'E':
            end_node = (x,y)
            h = 'z'
        heightmap[(x,y)] = ord(h)

graph = Graph(heightmap)

print(graph.bsf(end_node, start_node))
print(graph.bsf(end_node, start_node, True))