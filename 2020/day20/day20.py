import re 
from collections import defaultdict
from collections import deque
import operator
import queue

test_data = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

class Tile:
    all_tiles = {}
    side_size = 0
    edge_hash = defaultdict(list)
    tile_positions = {}
    corners = [ ]

    @staticmethod
    def find_corners():
        for tile in Tile.all_tiles.values():
            shared = 0
            for index in range(0, 4):
                if len(Tile.edge_hash[tile.tile_edge_hashes[index]]) == 2:
                    shared += 1
            if shared == 2:
                Tile.corners.append(tile)


    @staticmethod
    def assemble_tiles():
        # knowing what tiles are adjacent to other tiles using our dict, we
        # can place the upper left and then work on placing the rest
        Tile.find_corners()
        corner = Tile.corners[0]
        while len(Tile.edge_hash[corner.tile_edge_hashes[TOP]]) == 2 or len(Tile.edge_hash[corner.tile_edge_hashes[LEFT]]) == 2:
            corner.rotate(1)
        Tile.tile_positions[(0, 0)] = corner

        num_tiles = len(Tile.all_tiles)
        Tile.side_size = int(num_tiles ** 0.5)
        for index in range(1, len(Tile.all_tiles)):
            row = index // Tile.side_size 
            col = index % Tile.side_size 

            # just match the tile to the left or the top
            if col > 0:
                placed_tile = Tile.tile_positions[(row, col - 1)]
                placed_tile_hash = placed_tile.tile_edge_hashes[RIGHT]
                assert(len(Tile.edge_hash[placed_tile_hash]) == 2)
                new_tile_num = [ i for i in Tile.edge_hash[placed_tile_hash] if i != placed_tile.tile_num ]
                assert(len(new_tile_num) == 1)
                new_tile = Tile.all_tiles[new_tile_num[0]]

                # need to rotate the tile to place to match the has to the left
                position = new_tile.tile_edge_hashes.index(placed_tile_hash)

                # not in position, then rotate
                if position != LEFT:
                    difference = abs(LEFT - position)
                    new_tile.rotate(difference)

                # check to see if we need to flipa
                placed_side = [ d[-1] for d in placed_tile.tile_data ]
                new_side = [ d[0] for d in new_tile.tile_data ]

            else:
                placed_tile = Tile.tile_positions[(row - 1, col)]
                placed_tile_hash = placed_tile.tile_edge_hashes[BOTTOM]
                assert(len(Tile.edge_hash[placed_tile_hash]) == 2)
                new_tile_num = [ i for i in Tile.edge_hash[placed_tile_hash] if i != placed_tile.tile_num ]
                assert(len(new_tile_num) == 1)
                new_tile = Tile.all_tiles[new_tile_num[0]]

                # need to rotate the tile to place to match the has to the left
                position = new_tile.tile_edge_hashes.index(placed_tile_hash)

                # not in position, then rotate
                if position != TOP:
                    difference = 4 - position
                    new_tile.rotate(difference)

                # check to see if we need to flipa
                placed_side = placed_tile.tile_data[-1]
                new_side = new_tile.tile_data[0]

            if placed_side != new_side:
                new_tile.flip(col)

            for tile in Tile.tile_positions.values():
                assert(tile.tile_num != new_tile.tile_num)

            Tile.tile_positions[(row, col)] = new_tile

        # here, we have all the tiles placed, so now we can remove the borders from each tile
        for tile in Tile.all_tiles.values():
            new_data = [ '' ] * (tile.tile_size - 2)
            for index in range(1, tile.tile_size - 1):
                new_data[index - 1] = tile.tile_data[index][1:-1]
            tile.tile_data = new_data
            tile.tile_size -= 2

        # now place all tiles in an image for searching
        tile_size = Tile.corners[0].tile_size
        Tile.image = [''] * (Tile.side_size * tile_size)
        for row in range(0, Tile.side_size):
            for col in range(0, Tile.side_size):
                for trow in range(0, tile_size):
                    Tile.image[(row * tile_size) + trow] += Tile.tile_positions[(row, col)].tile_data[trow]

    def __init__(self, tile_num, tile_data):
        self.tile_num = tile_num
        Tile.all_tiles[self.tile_num] = self

        self.tile_data = tile_data
        self.tile_size = len(tile_data[0])
        assert(self.tile_size == len(tile_data))

        # calculate hashes for the sides to make it easier to 
        # put the puzzle together.  top, right, bottom, left
        top_hash = hash(tile_data[0]) + hash(tile_data[0][::-1])
        right_hash = hash(''.join(d[-1] for d in tile_data)) + hash(''.join(d[-1] for d in reversed(tile_data)))
        bottom_hash = hash(tile_data[-1]) + hash(tile_data[-1][::-1])
        left_hash = hash(''.join(d[0] for d in tile_data))  + hash(''.join(d[0] for d in reversed(tile_data)))
        self.tile_edge_hashes = deque([ top_hash, right_hash, bottom_hash, left_hash ])
        for h in self.tile_edge_hashes:
            Tile.edge_hash[h].append(self.tile_num)

    def rotate(self, num_rotates):
        for _ in range(0, num_rotates):
            self.tile_data = list(''.join(x[::-1]) for x in zip(*self.tile_data))
            self.tile_edge_hashes.rotate(1)

    def flip(self, col):
        # check to see if we are flipping on left or right side - so flip along Y axis
        if col != 0:
            self.tile_data = list(reversed(self.tile_data.copy()))
            saved = self.tile_edge_hashes[BOTTOM]
            self.tile_edge_hashes[BOTTOM] = self.tile_edge_hashes[TOP]
            self.tile_edge_hashes[TOP] = saved

        else:
            # flip along X axis
            self.tile_data = [ x[::-1] for x in self.tile_data ]
            saved = self.tile_edge_hashes[RIGHT]
            self.tile_edge_hashes[RIGHT] = self.tile_edge_hashes[LEFT]
            self.tile_edge_hashes[LEFT] = saved


if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n\n')
    for d in data:
        number, *lines = d.splitlines()
        lines = [ l for l in lines ]
        tile = Tile(int(number[5:-1]), lines )

    Tile.assemble_tiles() 
    print(Tile.corners[0].tile_num * Tile.corners[1].tile_num * Tile.corners[2].tile_num * Tile.corners[3].tile_num)

    monster_pattern = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    ]
    monster_coords = [ (r, c) for r in range(len(monster_pattern)) for c in range(len(monster_pattern[0])) if monster_pattern[r][c] == '#' ]

    # iterate through the rows/columns, looking for 
    num_monsters = 0
    for index in range(0, 8):
        for row in range(0, len(Tile.image) - len(monster_pattern)):
            for col in range(0, len(Tile.image[0]) - len(monster_pattern[0])):
                    if all(Tile.image[row + dr][col + dc] == '#' for dr, dc in monster_coords):
                        num_monsters += 1

        if num_monsters > 0:
            break

        if index == 4:
            Tile.image = [ x[::-1] for x in Tile.image ]


        # need to rotate the image and try again
        Tile.image = list(''.join(x[::-1]) for x in zip(*Tile.image))

    roughness = sum(row.count('#') for row in Tile.image)
    roughness -= (num_monsters * len(monster_coords))

    print(roughness)
