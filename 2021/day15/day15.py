from aocd import lines
from typing import List, Tuple
from collections import defaultdict
from queue import PriorityQueue

import sys
sys.path.append('../..')
import utils

def parse_lines(lines: str) -> dict:
    # create an int dict and then "surround" the points
    # the 9's which will prevent flood filling ouf of the
    # grid
    graph = defaultdict(int)
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            graph[(x, y)] = int(lines[y][x])

    return graph, len(lines[0])

def calculate_weight(graph: dict, new_point: Tuple, data_size:int, graph_size: int) -> int:
    # determine the new value for this graph element
    x = new_point[0]
    y = new_point[1]

    x_count = x // data_size 
    while x > data_size - 1:
        x -= data_size 

    y_count = y // data_size 
    while y > data_size - 1:
        y -= data_size 

    new_weight = graph[(x,y)] + x_count + y_count
    while new_weight >= 10:
        new_weight -= 9 
    return  new_weight


# directions to search from current node
dirs = [ (0, -1), (-1, 0), (1, 0), (0, 1) ]

def graph_search(graph: dict, data_size : int, graph_size: int, expand_graph = False) -> int:
    # set up dijkstra
    end = (graph_size - 1, graph_size - 1)

    start = (0,0)

    vertex_queue = PriorityQueue()
    vertex_queue.put((0, start))
    visited = {start, }

    while vertex_queue:
        priority, u = vertex_queue.get()

        # if we are at the end, then we are done
        if u == end:
            return priority

        for n in  [ (u[0] + d[0], u[1] + d[1]) for d in dirs ]:
            # skip any points not in the graph
            if n in visited:
                continue

            # if we are just doing the origina graph, then ignore
            # any points out of the graph
            if n not in graph and expand_graph == False:
                continue
            elif n not in graph:
                if n[0] < 0 or n[0] >= graph_size or n[1] < 0 or n[1] >= graph_size:
                    continue
                graph[n] = calculate_weight(graph, n, data_size, graph_size)

            weight = graph[n]
            vertex_queue.put((priority + weight, n))
            visited.add(n)


    return -1 

test_lines = [
    '1163751742',
    '1381373672',
    '2136511328',
    '3694931569',
    '7463417111',
    '1319128137',
    '1359912421',
    '3125421639',
    '1293138521',
    '2311944581',
]
if __name__ == '__main__': 
    graph, size= parse_lines(lines)
    print(graph_search(graph, size, size))
    print(graph_search(graph, size, size * 5, True))


# from queue import PriorityQueue

# matrix = [list(map(int, line)) for line in lines]

# # solved using priority queue
# def solve_dis(m):
#     h, w = len(m), len(m[0])
#     pq = PriorityQueue()
#     # Add starting position in priority queue
#     pq.put((0, (0, 0)))
#     visited = {(0, 0), }
#     while pq:
#         curr_risk, (i, j) = pq.get()
#         # Once we reach the end of the matrix, we can stop and return the risk
#         if i == h - 1 and j == w - 1:
#             return curr_risk
#         for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
#             if 0 <= x < h and 0 <= y < w and (x, y) not in visited:
#                 weight = m[x][y]
#                 pq.put((curr_risk + weight, (x, y)))
#                 visited.add((x, y))


# def make_big_matrix():
#     # Using dict to map weights {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 1}
#     d = {i: j % 10 if j % 10 != 0 else 1 for i, j in zip(range(1, 10), range(2, 11))}
#     big_matrix = [lst.copy() for lst in matrix]
#     for _ in range(4):
#         for i in range(len(matrix)):
#             for j in range(len(matrix[0])):
#                 big_matrix[i].append(d[big_matrix[i][j + len(matrix) * _]])
#     for _ in range(4):
#         for i in range(len(matrix)):
#             new_list = list()
#             for j in range(len(big_matrix[0])):
#                 new_list.append(d[big_matrix[i + len(matrix) * _][j]])
#             big_matrix.append(new_list)
#     return big_matrix


# print(f'Part 1 : {solve_dis(matrix)}')
# print(f'Part 2 : {solve_dis(make_big_matrix())}')