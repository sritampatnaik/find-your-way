import sys
import Queue
import distanceAngleCalculation
from jsonParser import mapParser

currMap = mapParser(1, 2)
NUM_NODES = currMap.numElements

visitedNodes = [0 for x in range(NUM_NODES)] #here we store whether we have visited a certain node
nodes = [0 for x in range(NUM_NODES)] #we store the shortest path from the root node
tree = []


def init():
    for x in range(0, NUM_NODES):
        nodes[x] = sys.maxint
        visitedNodes[x] = 0

def isAllRed():
    for x in visitedNodes:
        if x == 0:
            return 0
    return 1

def setMap(buildingNo, levelNo):
    global currMap
    global NUM_NODES
    global visitedNodes
    global nodes
    global tree
    currMap = mapParser(buildingNo, levelNo)
    NUM_NODES = currMap.numElements
    visitedNodes = [0 for x in range(NUM_NODES)]  # here we store whether we have visited a certain node
    nodes = [0 for x in range(NUM_NODES)]  # we store the shortest path from the root node
    tree = []

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



