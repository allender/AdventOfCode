from aocd.models import Puzzle
import re

puzzle = Puzzle(2023, 2)
lines = puzzle.input_data.splitlines()
#lines = puzzle.examples[0][0].splitlines()

MAX_RED = 12
MAX_BLUE = 14
MAX_GREEN = 13

re_reds = re.compile(r'(\d*) red')
re_blues = re.compile(r'(\d*) blue')
re_greens = re.compile(r'(\d*) green')

def do_draw():
    game_total = 0
    total_power = 0
    for game_num, l in enumerate(lines):
        data = l.split(':')

        reds = re_reds.findall(data[1])
        blues = re_blues.findall(data[1])
        greens = re_greens.findall(data[1])

        max_red = max([ int(x) for x in reds ])
        max_blue = max([ int(x) for x in blues ])
        max_green = max([ int(x) for x in greens ])

        if max_red <= MAX_RED and max_blue <= MAX_BLUE and max_green <= MAX_GREEN:
            game_total += (game_num + 1)

        total_power += max_red * max_blue * max_green

    print(game_total)
    print(total_power)


do_draw()