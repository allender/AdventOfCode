# pylint: disable=missing-docstring, unused-import, mixed-indentation

import sys
import os
import re
import itertools
import math
import functools

def lcm(nums):
    return functools.reduce(lambda a, b: a * b // math.gcd(a, b), nums)

class Moon():
    period = [ 0, 0, 0 ]

    def __init__(self, x, y, z):
        self.pos = [ x, y, z ]
        self.velocity = [ 0, 0, 0 ]
        self.potential_energy = 0
        self.kinetic_energy = 0
        self.total_energy = 0

        self.original_pos = self.pos.copy( )
        self.original_velocity = self.velocity.copy( )

    def __repr__(self):
        return 'pos: {0}\tvel: {1}'.format(self.pos, self.velocity)

    def step(self, other_moon):
        for i in range(3):
            diff = other_moon.pos[i] - self.pos[i]
            if (diff < 0):
                self.velocity[i] -= 1
                other_moon.velocity[i] += 1
            elif (diff > 0):
                self.velocity[i] += 1
                other_moon.velocity[i] -= 1

    def apply_velocity( self ):
        for i in range(3):
            self.pos[i] += self.velocity[i]

    def calculate_energy( self ):
        self.potential_energy = abs(self.pos[0]) + abs(self.pos[1]) + abs(self.pos[2])
        self.kinetic_energy = abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])
        self.total_energy = self.potential_energy * self.kinetic_energy

def part1( positions ):
    moons = [ ]
    for pos in positions:
        vals = list(map(int,re.match('.*\=([-]*\d*).*\=([-]*\d*).*\=([-]*\d*).*', pos).groups()))
        moons.append( Moon(vals[0], vals[1], vals[2]) )

    # run steps and calculate velcoties
    # part 1
    numsteps = 1000
    for num in range(1 , numsteps + 1):
        for pairs in itertools.combinations( moons, 2 ):
            pairs[0].step( pairs[1] )

        for moon in moons:
            moon.apply_velocity( )

        for moon in moons:
            moon.calculate_energy( )

    return sum( [ x.total_energy for x in moons ] )

def part2( positions ):
    # figure each position independently
    moons = [ ]
    for pos in positions:
        vals = list(map(int,re.match('.*\=([-]*\d*).*\=([-]*\d*).*\=([-]*\d*).*', pos).groups()))
        moons.append( Moon(vals[0], vals[1], vals[2]) )

    period = 0
    while( True ):
        for pairs in itertools.combinations( moons, 2 ):
            pairs[0].step( pairs[1] )

        for moon in moons:
            moon.apply_velocity( )

        period += 1

        for i in range(3):
            if all( [(x.pos[i] == x.original_pos[i] and x.velocity[i] == x.original_velocity[i]) for x in moons ] ) and Moon.period[i] == 0:
                Moon.period[i] = period

        if all( [ x != 0 for x in Moon.period ] ):
            break


    return (lcm(Moon.period))

if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        positions = f.readlines()

    # part 1
    print ( part1( positions ) )
        
    # part 2
    print ( part2( positions ) )

