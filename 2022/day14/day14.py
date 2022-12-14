from aocd.models import Puzzle
import re
import functools

puzzle = Puzzle(year=2022, day = 14)

test_data = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''

class Cave():
    def __init__(self, data, sand_start, part2 = False):
        self.part2 = part2
        self.cells = {}
        self.sand_count = 0
        self.sand_start = sand_start
        self.minx = self.sand_start[0]
        self.miny = self.sand_start[1]
        self.maxx = -self.sand_start[0] 
        self.maxy = -self.sand_start[1] 

        for l in data.splitlines():
            points = [ tuple(map(int, p.split(','))) for p in re.findall(r'\d+,\d+', l) ]
            for p in points:
                self.minx = min(p[0], self.minx)
                self.miny = min(p[1], self.miny)
                self.maxx = max(p[0], self.maxx)
                self.maxy = max(p[1], self.maxy)

            first_point = points[0]
            for next_point in points[1:]:
                # y values are the same
                if first_point[1] == next_point[1]:
                    start, end = sorted((first_point[0], next_point[0]))
                    for x in range(start, end + 1):
                        self.cells[(x, first_point[1])] = '#'

                # x values are the same 
                elif first_point[0] == next_point[0]:
                    start, end = sorted((first_point[1], next_point[1]))
                    for y in range(start, end + 1):
                        self.cells[(first_point[0], y)] = '#'

                # process the next pair
                first_point = next_point

        # for part 2, add in a floor at max y + 2
        if self.part2 == True:
            self.maxy = self.maxy + 1

    def drop_sand(self, sand_pos):
        self.sand_count += 1
        while(True):
            if self.part2 == False:
                if sand_pos[0] <= self.minx or sand_pos[1] >= self.maxy:
                    self.sand_count -= 1
                    return False
            
            elif sand_pos[1] == self.maxy:
                self.cells[sand_pos] = 'o'
                return True

            if (sand_pos[0], sand_pos[1] + 1) not in self.cells:
                sand_pos = (sand_pos[0], sand_pos[1] + 1)
                continue

            # move to the lower left
            if (sand_pos[0] - 1, sand_pos[1] + 1) not in self.cells:
                sand_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
                continue
            
            # move to the lower right
            if (sand_pos[0] + 1, sand_pos[1] + 1) not in self.cells:
                sand_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
                continue

            if sand_pos == self.sand_start:
                return False

            self.cells[sand_pos] = 'o'
            return True
            

    def run_sim(self):
        simulating = True
        while(simulating):
            simulating = self.drop_sand(self.sand_start)


    def __repr__(self):
        map = ''
        for y in range(self.miny, self.maxy+1, 1):
            s = ''
            for x in range(self.minx, self.maxx + 1, 1):
                if (x,y) in self.cells:
                    s += self.cells[(x,y)]
                else:
                    s += '.'

            map += s
            map += '\n'

        return map



cave = Cave(puzzle.input_data, (500, 0))
cave.run_sim()
print(cave.sand_count)

# start over for part 2
cave = Cave(puzzle.input_data, (500, 0), True)
cave.run_sim()
print(cave.sand_count)
