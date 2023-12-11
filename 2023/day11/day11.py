from aocd.models import Puzzle
from itertools import combinations, starmap

puzzle = Puzzle(2023, 11)

input = puzzle.input_data.split('\n')
# input = puzzle.examples[0][0].split('\n')

class Universe():
    def __init__(self, input):
        self.universe = []
        for l in input:
            self.universe.append(list(l))

        # find empty rows
        self.empty_rows = [ index_y for index_y,y in enumerate(self.universe) if y.count('.') == len(y) ]
        self.empty_columns = []
        for index_x in range(len(input)):
            if all(y[index_x] == '.' for y in self.universe):
                self.empty_columns.append(index_x)

        # find the  galaxies and number them
        self.galaxies = [(x_index,y_index) for y_index, y in enumerate(self.universe) for x_index, x in enumerate(y) if x == '#']

    def find_manhatten(self, expansion_val):
        pairs = combinations(self.galaxies, 2)
        def compute(x, y):
            dist = abs(x[0] - y[0]) + abs(x[1] - y[1])

            # figure out how many empty rows and colums between
            dist += sum(expansion_val - 1 for c in self.empty_columns if min(x[0], y[0]) < c < max(x[0], y[0]))
            dist += sum(expansion_val - 1 for r in self.empty_rows if min(x[1], y[1]) < r < max(x[1], y[1]))
            return dist

        self.distances = [ x for x in starmap(compute, pairs) ]

    def __repr__(self):
        result = ''
        for y in self.universe:
            for x in y:
                result += str(x)

            result += '\n'
        result += '\n'
        return result


universe = Universe(input)
universe.find_manhatten(2)
print(sum(universe.distances))
universe.find_manhatten(1000000)
print(sum(universe.distances))