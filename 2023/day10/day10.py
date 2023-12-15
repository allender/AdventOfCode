from aocd.models import Puzzle

puzzle = Puzzle(2023, 10)

input = puzzle.input_data.split('\n')
# input = puzzle.examples[0][0].split('\n')

dirs = {
    '|': (-1j, 1j),
    '-': (-1, 1),
    'L': (-1j, 1),
    'J': (-1j, -1),
    '7': (-1, 1j),
    'F': (1, 1j),
    'S': (1, 1j, -1, -1j),
    '.': ()
}

maze = {complex(j,i): c for i,r in enumerate(input) for j,c in enumerate(r.strip())}
graph = {p: {p+d for d in dirs[c]} for p,c in maze.items()}
# start = complex(1, 1)
start = [ p for p,d in graph.items() if len(d) == 4][0]

path = []
current = start
while True:
    path.append(current)
    next_nodes = graph[current]
    next = [ n for n in next_nodes if n not in path and n in graph and len(graph[n]) > 0 ]
    if len(next) == 0:
        if len(next_nodes) !=0 and start not in next_nodes:
            assert(0)
        break
    if current == start:
        current = next[2]
    else:
        current = next[0]

print((len(path))//2)

# use the shoelace theorm to find the area inside
path.append(path[0])
area = abs(0.5 * sum(a.real*b.imag - a.imag*b.real for a,b in zip(path, path[1:])))
print(area - len(path)//2 + 1)
