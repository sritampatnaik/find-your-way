import sys
import Queue
import distanceAngleCalculation
from jsonParser import mapParser
import os

### This code is suppossed to be uncommented out in the pi ###
import communication
Comm = communication.Comm()

confirm = ""
while confirm != "*":
    buildingName = ""
    levelNo = ""
    print "Enter building number: "
    os.system('flite -t "Enter building number:" ')
    while buildingName == "":
        buildingName = Comm.get_keypad_input()

    os.system("flite -t 'You entered " + str(buildingName) + "'")
    print buildingName

    print "Level Num: "
    os.system('flite -t "Enter Level Number:" ')
    while levelNo == "":
        levelNo = Comm.get_keypad_input()

    os.system("flite -t 'You entered " + str(levelNo) + "'")
    print levelNo

    os.system('flite -t "Press star and hash to confirm:" ')
    while confirm == "":
        confirm = Comm.get_keypad_input()

os.system('flite -t "You have confirmed" ')

### The following code is for debugging in the ide so comment it in the pi ###
# confirm = ""
# while confirm != "*":
#     buildingName = ""
#     levelNo = ""
#     print "Enter building number: "
#     while buildingName == "":
#         buildingName = input()
#
#     print buildingName
#
#     print "Level Num: "
#     while levelNo == "":
#         levelNo = input()
#
#     print levelNo
#     confirm = raw_input("confirm:")


currMap = mapParser(buildingName,levelNo)
NUM_NODES = currMap.numElements


visitedNodes = [0 for x in range(NUM_NODES)] #here we store whether we have visited a certain node
nodes = [0 for x in range(NUM_NODES)] #we store the shortest path from the root node
tree = []


def init():
    for x in range(0, NUM_NODES):
        nodes[x] = sys.maxint
        visitedNodes[x] = 0


##        for y in range(0, NUM_NODES):
##            adj[x][y] = -1
##            adj[0][2] = 5
##            adj[1][0] = 1
##            adj[1][4] = 1
##            adj[1][5] = 3
##            adj[2][1] = 3
##            adj[2][3] = 5
##            adj[2][4] = 1
##            adj[4][3] = 2
##            adj[4][5] = 4

def isAllRed():
    for x in visitedNodes:
        if x == 0:
            return 0
    return 1


def getMinDistNode():
    minDist = sys.maxint
    minIndex = -1
    for x in range(NUM_NODES):
        if visitedNodes[x] == 0 and nodes[x] < minDist:
            minIndex = x
            minDist = nodes[x]
    return minIndex


def relax(v, w):
    d = nodes[v] + currMap.getDistance(v, w)  # adj[v][w]
    if nodes[w] > d:
        nodes[w] = d
        newEdge = [v, w]
        isFound = 0
        for x in tree:
            if x[1] == w:
                x[0] = v
                isFound = 1
        if isFound == 0:
            tree.append(newEdge)


def dijkstra(start):
    init()
    nodes[start] = 0

    while (isAllRed() == 0):
        v = getMinDistNode()
        visitedNodes[v] = 1

        for w in range(NUM_NODES):
            if w != v and currMap.getDistance(v, w) > 0:
                relax(v, w)
    # print "Distance:", nodes
    # print
    # print "Tree:", tree
    # print


def isInTree(start, end):
    for x in tree:
        if x[0] == start and x[1] == end:
            return True
    return False

def getCurrMap():
    return currMap

def getPath(start, end):
    init()
    path = [start]

    while path[len(path) - 1] != end:
        isFound = False
        for x in tree:
            if x[0] == path[len(path) - 1] and visitedNodes[x[1]] == 0:
                path.append(x[1])
                isFound = True
                break
        if not isFound:
            visitedNodes[path.pop()] = 1
    return path        





