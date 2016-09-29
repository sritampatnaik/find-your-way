import sys
import Queue
import distanceAngleCalculation
from jsonParser import mapParser

# [[0 for x in range(NUM_NODES)] for x in range(NUM_NODES)]

mapNo = input("Map No: ")
while (True):
    if mapNo == 0:
        currMap = mapParser("com1L2")
        NUM_NODES = currMap.numElements
        # adj = com1L2.matrix
        break
    elif mapNo == 1:
        currMap = mapParser("com2L2")
        NUM_NODES = currMap.numElements
        # adj = com1L2.matrix
        break
    elif mapNo == 2:
        currMap = mapParser("com2L3")
        NUM_NODES = currMap.numElements
        # adj = com1L2.matrix
        break
    else:
        mapNo = input("Map No: ")

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
    # print "Path:",  # path
    # for x in range(len(path)):
    #     print path[x] + 1,

startingNode = input("Starting Node: ")
endingNode = input("Ending Node: ")
dijkstra(startingNode - 1)
path = getPath(startingNode - 1, endingNode - 1)
print "Path:",  # path
for x in range(len(path)):
    print path[x] + 1,
print

for x in range(0, 5):
    currX = input("Current X: ")
    currY = input("Current Y: ")
    currHeading = int(input("Current Heading: "))
    nearestNode = path[0]+1
    minDis = distanceAngleCalculation.distance(currX, currY, currMap.buildingMap['map'][path[0]]['x'], currMap.buildingMap['map'][path[0]]['y'])
    currAngle = distanceAngleCalculation.calcAngle(int(currX), int(currY), int(currMap.buildingMap['map'][path[0]]['x']), int(currMap.buildingMap['map'][path[0]]['y']), int(currMap.buildingMap['info']['northAt']))

    for x in range(len(path)):
        if minDis > distanceAngleCalculation.distance(currX, currY, currMap.buildingMap['map'][path[x]]['x'], currMap.buildingMap['map'][path[x]]['y']):
            nearestNode = path[x]+1
            minDis = distanceAngleCalculation.distance(currX, currY, currMap.buildingMap['map'][path[x]]['x'], currMap.buildingMap['map'][path[x]]['y'])
            currAngle = distanceAngleCalculation.calcAngle(int(currX), int(currY), int(currMap.buildingMap['map'][path[x]]['x']), int(currMap.buildingMap['map'][path[x]]['y']), int(currMap.buildingMap['info']['northAt']))

    turnAngle = 0
    turnDirection = ''
    if (currAngle - currHeading) < -180:
        turnAngle = (currAngle - currHeading) + 360
    else:
        turnAngle = currAngle - currHeading

    if turnAngle < 0 :
        turnDirection = 'left'
    else:
        turnDirection = 'right'

    print 'Turn ' + turnDirection + ' by ' + str(abs(turnAngle)) + ' degrees and walk '+ str(minDis) + ' cms to the nearest node which is ' + str(nearestNode)



