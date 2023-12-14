from aocd.models import Puzzle

puzzle = Puzzle(2023, 14)

rocks = puzzle.input_data.split('\n')
# rocks = puzzle.examples[0][0].split('\n')

def roll_rocks(rocks, left):
    rolled_rocks = []
    for r in rocks:
        sections = r.split('#')
        new_sections = []
        for s in sections:
            if left == True:
                new_sections.append('O' * s.count('O') + '.' * (len(s) - s.count('O')))
            else:
                new_sections.append('.' * (len(s) - s.count('O')) + 'O' * s.count('O'))

        rolled_rocks.append('#'.join(new_sections))

    return rolled_rocks

tilted_rocks = roll_rocks( [''.join(x) for x in zip(*rocks)], True )
post_tilted_rocks =  [ ''.join(x) for x in zip(*tilted_rocks)]
print(sum(l.count('O') * (len(post_tilted_rocks) - index) for index, l in enumerate(post_tilted_rocks)))

rocks_cache = []
score_cache = []
for index in range(1000000000):
    # tilt north
    rocks = roll_rocks( [''.join(x) for x in zip(*rocks)], True )
    rocks =  [ ''.join(x) for x in zip(*rocks)]

    # west  
    rocks = roll_rocks( rocks, True )

    # south 
    rocks = roll_rocks( [''.join(x) for x in zip(*rocks)], False )
    rocks =  [ ''.join(x) for x in zip(*rocks)]

    #west 
    rocks = roll_rocks( rocks, False )

    # if we are here, we have started looping the
    # rock layouts so we can callculate the actual  score
    score = sum(l.count('O') * (len(rocks) - index) for index, l in enumerate(rocks))
    if rocks in rocks_cache:
        loop_start = rocks_cache.index(rocks)
        loop_length = index - rocks_cache.index(rocks)
        loc = (1000000000 - (loop_start+1)) % loop_length
        print(score_cache[loop_start + loc])
        break

    rocks_cache.append(rocks)
    score_cache.append(score)
