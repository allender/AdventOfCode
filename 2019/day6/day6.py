# pylint: disable=missing-docstring, unused-import
  
import sys

class Orbit():
    def __init__( self, name, parent = None ):
        self.name = name 
        self.parent = parent
        self.orbiters = [ ]

    def __repr__(self):
        return self.name

    def addOrbiter( self, orbiter ):
        self.orbiters.append( orbiter )

    def getOrbiters( self ):
        return self.orbiters

def createTree(root, orbits ):
    c = root.name
    orbiters = orbits.get( c, [ ] )
    for o in orbiters:
        newOrbit = Orbit(o, root)
        root.addOrbiter(newOrbit)
        createTree(newOrbit, orbits)

def printOrbits(root):
    print('{0}: {1}'.format(root.name, root.orbiters) )
    for o in root.orbiters:
        printOrbits(o)

def calcNumberOrbits(root, level):
    num = len(root.orbiters)
    for o in root.orbiters:
        num += level
        num += calcNumberOrbits(o, level + 1)

    return num


def findOrbit(root, whichOrbit):
    if (root.name == whichOrbit):
        return root

    for o in root.orbiters:
        santa = findOrbit(o, whichOrbit)
        if santa is not None:
            return santa

    return None

def getPathToRoot(node):
    path = [ ]
    while (node.parent is not None):
        path.append(node.parent)
        node = node.parent

    return path
    

def findDistance(orbit1, orbit2):
    path1 = getPathToRoot(orbit1)
    path2 = getPathToRoot(orbit2)    

    # with the two paths, find the common root
    # and determien the distance to each leaf
    # from tehre
    for r1 in path1:
        if r1 in path2:
            break

    dist1 = path1.index(r1)
    dist2 = path2.index(r1)

    return dist1 + dist2

if __name__ == '__main__':
    with open('input.txt') as f:
        readlines = f.readlines()

    lines = [ l.strip() for l in readlines ]

    orbits = { }

    for l in lines:
        center, planet = l.split(')')
        orbits.setdefault(center, []).append( planet )

    # create the tree for the orbitsq
    orbitRoot = Orbit( 'COM' )
    createTree(orbitRoot, orbits)

    # calculate total number of direct and indirect orbits
    printOrbits(orbitRoot)
    numOrbits = calcNumberOrbits(orbitRoot, 0)
    print (numOrbits)

    santaOrbit = findOrbit(orbitRoot, 'SAN')
    youOrbit = findOrbit(orbitRoot, 'YOU')
    print (santaOrbit)
    print (youOrbit)

    length = findDistance(santaOrbit, youOrbit)
    print (length)