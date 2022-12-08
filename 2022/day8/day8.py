from aocd.models import Puzzle
from collections import defaultdict

puzzle = Puzzle(year=2022, day = 8)

data = puzzle.input_data

map = defaultdict(int)
lines = data.splitlines()
width = len(lines)
height = len(lines)

def is_tree_visible(x, y):
    # up
    visible = True
    for y1 in range(y - 1, -1, -1):
        if map[(x, y1)] >= map[(x,y)]:
            visible = False
            break

    if visible:
        return True
            
    # down
    visible = True
    for y1 in range(height - 1, y, -1):
        if map[(x, y1)] >= map[(x,y)]:
            visible = False
            break

    if visible:
        return True

    # left
    visible = True
    for x1 in range(x - 1, -1, -1):
        if map[(x1, y)] >= map[(x,y)]:
            visible = False
            break
    
    if visible:
        return True

    # right
    visible = True
    for x1 in range(width - 1, x, -1):
        if map[(x1, y)] >= map[(x,y)]:
            visible = False
            break

    return visible

def calculate_sceneic_scores():

    def get_score(x,y):
        visible_up = 1  
        for y1 in range(y - 1, 0, -1):
            if map[(x, y1)] >= map[(x,y)]:
                break
            visible_up  += 1
        
        # down
        visible_down = 1
        for y1 in range(y+1, height - 1):
            if map[(x, y1)] >= map[(x,y)]:
                break
            visible_down += 1

        # left
        visible_left = 1
        for x1 in range(x - 1, 0, -1):
            if map[(x1, y)] >= map[(x,y)]:
                break
            visible_left += 1
        
        # right
        visible_right = 1
        for x1 in range(x + 1, width - 1):
            if map[(x1, y)] >= map[(x,y)]:
                break
            visible_right += 1

        return visible_left * visible_right * visible_up * visible_down

    scores = []
    for y in range(1, width - 1):
        for x in range(1, height - 1):
            scores.append(get_score(x,y))

    return max(scores)


for y, l in enumerate(lines):
    for x, tree in enumerate(l):
        map[(x,y)] = tree

visible_trees = []
for y in range(1, width - 1):
    for x in range(1, height - 1):
        if is_tree_visible(x,y) == True:
            visible_trees.append((x,y))

print(len(visible_trees) + width + height + width - 2 + height - 2)

print(calculate_sceneic_scores())
