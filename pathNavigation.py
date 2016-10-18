from jsonParser import mapParser
from communication import Comm
import distanceAngleCalculation
import djikstra
import math
import time


def giveDirection():
    nextUnvisitedNode = path[nextNodeIndex]+1
    minDis = distanceAngleCalculation.distance(currX, currY, currMap.buildingMap['map'][path[nextNodeIndex]]['x'], currMap.buildingMap['map'][path[nextNodeIndex]]['y'])
    currAngle = distanceAngleCalculation.calcAngle(int(currX), int(currY), int(currMap.buildingMap['map'][path[nextNodeIndex]]['x']), int(currMap.buildingMap['map'][path[nextNodeIndex]]['y']), int(currMap.buildingMap['info']['northAt']))

    turnAngle = 0
    turnDirection = ''

    if (currAngle - currHeading) < -180:
        turnAngle = (currAngle - currHeading) + 360
    else:
        turnAngle = currAngle - currHeading

    if turnAngle < 0:
        turnDirection = 'left'
    else:
        turnDirection = 'right'

    print 'Turn ' + turnDirection + ' by ' + str(abs(turnAngle)) + ' degrees and walk '+ str(minDis) + ' cms to node ' + str(nextUnvisitedNode)


def isAtNextNode():
    disToNextNode = distanceAngleCalculation.distance(currX, currY, currMap.buildingMap['map'][path[nextNodeIndex]]['x'], currMap.buildingMap['map'][path[nextNodeIndex]]['y'])
    if disToNextNode < 51:
        return True
    return False


def updateCoordinates(distanceWalked, currHeading):
    global currX
    global currY
    # calculate angle of triangle
    theta = currHeading - 135

    # take abs values in case angle is not acute. walker is a cock.
    deltaX = math.fabs(distanceWalked * math.cos(math.radians(theta)))
    deltaY = math.fabs(distanceWalked * math.sin(math.radians(theta)))

    # update coordinates
    if -90 < theta <= 0:
        currX += float(deltaX)
        currY += deltaY
    elif -180 < theta <= -90:
        currX -= deltaX
        currY += deltaY
    elif 0 < theta <= 90:
        currX += deltaX
        currY -= deltaY
    elif 90 < theta <= 180:
        currX -= deltaX
        currY -= deltaY


startingNode = input("Starting Node: ")
endingNode = input("Ending Node: ")
djikstra.dijkstra(startingNode - 1)
path = djikstra.getPath(startingNode - 1, endingNode - 1)
currMap = djikstra.getCurrMap()
print "Path:",  # path
for x in range(len(path)):
    print path[x] + 1,

nextNodeIndex = 1
currX = int(currMap.buildingMap['map'][path[0]]['x'])
currY = int(currMap.buildingMap['map'][path[0]]['y'])

Comm.start_sensing()
Comm.request_data()
currHeading = Comm.get_heading()
giveDirection()

while (nextNodeIndex != len(path)):
    while not (isAtNextNode()):
        # Uncomment the code below to implement step counter
        # distancewalked = input("Distance Walked:")
        # currHeading = input("Current Heading: ")
        time.sleep(2)  # delays for 5 seconds
        Comm.request_data()
        distancewalked = Comm.get_steps()
        currHeading = Comm.get_heading()
        updateCoordinates(distancewalked, currHeading)
        # Uncomment the code below to key in x and y manually
        # currX = input("Current X: ")
        # currY = input("Current Y: ")
        # currHeading = int(input("Current Heading: "))
        if isAtNextNode(): break;
        giveDirection()
    print "Reached: Node " + str(path[nextNodeIndex]+1)
    nextNodeIndex += 1

print "Reached end node, peace out !"


