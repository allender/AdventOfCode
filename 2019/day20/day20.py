# pylint: disable=missing-docstring, unused-import, mixed-indentation

import os
import sys
import collections
import queue

directions = [ (1, 0), (-1, 0), (0, 1), (0,-1) ]

Point = collections.namedtuple( 'Point', ['x', 'y'] )
State = collections.namedtuple( 'State', [ 'point', 'distance', 'warped' ] )
StateR = collections.namedtuple( 'State', [ 'point', 'distance', 'level', 'warped' ] )
Portal = collections.namedtuple( 'Portal', ['label', 'point', 'outer' ] )

# read the input
grid = []
for line in open('input.txt').readlines():
    grid.append(list(line.rstrip('\n')))

num_rows = len(grid)
num_columns = len(grid[0])

portals = collections.defaultdict(list)
for y in range(0, num_rows - 1):
    for x in range(0, num_columns -1):
        id = grid[y][x]
        id_down = grid[y+1][x]
        id_right = grid[y][x+1]

        # see if we have an id.  We will only look for the
        # topmost or leftmost character
        if id.isupper() and id_down.isupper():
            portal_id = id + id_down
            # need to figure out the portal point.  This is
            # a portal that is up and down (i.e. changes in Y direction)
            if y > 0 and grid[y-1][x] == '.':
                portals[portal_id].append( Point(x, y-1) )
            elif y < num_rows - 1 and grid[y+2][x] == '.':
                portals[portal_id].append( Point(x, y+2) )

        elif id.isupper() and id_right.isupper():
            portal_id = id + id_right
            # need to figure out the portal point.  This is
            # a portal that is right and left (i.e. changes in X direction)
            if x > 0 and grid[y][x-1] == '.':
                portals[portal_id].append( Point(x-1, y) )
            elif x < num_columns - 1 and grid[y][x+2]:
                portals[portal_id].append( Point(x+2, y) )

# create dictionary of portal to portal.  Include portal names (for debugging)
# as well as whether the portal is an outer or inner portal (for part 2)
portalmap = { }
for portal, locations in  portals.items():
    if len(locations) == 2:
        portal0_point = locations[0]
        portal1_point = locations[1]

        # need to determine which portal is inner and which is outer.  Check the first
        # portal and determine if that is in or out.  This is all needed for part 2
        outer = False
        if portal0_point.x == 2 or portal0_point.y == 2 or portal0_point.x == num_columns - 3 or portal0_point.y == num_rows - 3:
            outer = True
 
        portalmap[locations[0]] = Portal( portal, portal1_point, not outer )
        portalmap[locations[1]] = Portal( portal, portal0_point, outer )

def find_path_part1():
    start = portals['AA'][0]
    end = portals['ZZ'][0]

    states = collections.deque( [State(Point(start[0], start[1]), 0, False)] )
    visited = set( )
    while states:
        state = states.popleft( )

        if state.point == end:
            return state.distance

        if state.point in visited:
            continue

        visited.add( state.point )

        # is this space a portal.  only follow the portal if we didn't follow
        # one to get here
        dest_portal = portalmap.get( state.point )
        if dest_portal is not None and state.warped is False:
            states.append( State(Point(dest_portal.point.x, dest_portal.point.y), state.distance + 1, True) )

        else:
            for d in directions:
                new_x = state.point.x + d[0]
                new_y = state.point.y + d[1]
                if grid[new_y][new_x] == '.':
                    states.append( State(Point(new_x, new_y), state.distance + 1, False) )

print( find_path_part1() )

def find_path_part2():
    start = portals['AA'][0]
    end = portals['ZZ'][0]

    states = collections.deque( [StateR(Point(start[0], start[1]), 0, 0, False)] )
    visited = set( ) 
    while states:
        state = states.popleft( )

        if state.point == end and state.level == 0:
            return state.distance

        if (state.point, state.level) in visited:
            continue

        visited.add( (state.point, state.level) )

        # is this space a portal.  only follow the portal if we didn't follow
        # one to get here
        dest_portal = portalmap.get( state.point )

        if dest_portal is not None and state.warped is False and (state.level > 0 or dest_portal.outer is True):
            # going through portal we need to adjust the recusriveness of the maze
            # if the dest portal is an outside portal, then we decrement the level, otherwise
            # we increment
            new_level = max(0, state.level - 1)
            if dest_portal.outer is True:
                new_level = state.level + 1

            states.append( StateR(Point(dest_portal.point.x, dest_portal.point.y), state.distance + 1, new_level, True) )

        else:
            for d in directions:
                new_x = state.point.x + d[0]
                new_y = state.point.y + d[1]
                if grid[new_y][new_x] == '.':
                    new_point = Point(new_x, new_y)
                    if new_point != start and new_point != end or state.level == 0:
                        states.append( StateR(new_point, state.distance + 1, state.level, False) )

print( find_path_part2() )
