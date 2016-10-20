from jsonParser import mapParser
import communication
import distanceAngleCalculation
import djikstra
import math
import time
import os

Comm = communication.Comm()


def giveDirection():
    nextUnvisitedNode = path[nextNodeIndex] + 1
    minDis = distanceAngleCalculation.distance(currX, currY, currMap.buildingMap['map'][path[nextNodeIndex]]['x'],
                                               currMap.buildingMap['map'][path[nextNodeIndex]]['y'])
    currAngle = distanceAngleCalculation.calcAngle(int(currX), int(currY),
                                                   int(currMap.buildingMap['map'][path[nextNodeIndex]]['x']),
                                                   int(currMap.buildingMap['map'][path[nextNodeIndex]]['y']),
                                                   int(currMap.buildingMap['info']['northAt']))

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

    if abs(turnAngle) > 10:
        os.system("flite -t ' " + turnDirection + str(int(abs(turnAngle))) + " walk " + str(int(round(minDis / 42))) + " steps '")
        print  turnDirection + str(int(abs(turnAngle))) + ' walk ' + str(int(round(minDis/42))) + ' cms  '
    else:
        os.system("flite -t 'Walk straight " + str(int(round(minDis / 42))) + " steps'")
        print 'Walk straight ' + str(int(round(minDis / 42))) + ' steps '


def isAtNextNode():
    disToNextNode = distanceAngleCalculation.distance(currX, currY,
                                                      currMap.buildingMap['map'][path[nextNodeIndex]]['x'],
                                                      currMap.buildingMap['map'][path[nextNodeIndex]]['y'])
    if disToNextNode < 51:
        return True
    return False


def updateCoordinates(distanceWalked, currHeading):
    global currX
    global currY
    # calculate angle of triangle
    alpha = 360 - int(currMap.buildingMap['info']['northAt']) + 90
    if alpha > 429:
            alpha = alpha - 360
    theta = currHeading - alpha

    # take abs values in case angle is not acute. walker is a cock.
    deltaX = math.fabs(distanceWalked * math.cos(math.radians(theta)))
    deltaY = math.fabs(distanceWalked * math.sin(math.radians(theta)))

    # update coordinates
    if (-90 < theta <= 0) or (270 < theta <= 360):
        currX += float(deltaX)
        currY += deltaY
    elif (-180 < theta <= -90) or (180 < theta <= 270):
        currX -= deltaX
        currY += deltaY
    elif (-360 < theta <= -270) or (0 < theta <= 90):
        currX += deltaX
        currY -= deltaY
    elif (-180 < theta <= -270) or (90 < theta <= 180):
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
prevTotalDistance = 0

Comm.start_sensing()
Comm.request_data()
currHeading = Comm.get_heading()
currHeading = input("Heading:" )
giveDirection()

while (nextNodeIndex != len(path)):
    while not (isAtNextNode()):
        # Uncomment the code below to implement step counter
        # totalSteps = input("Total steps:")
        # currHeading = input("Heading:" )
        # print "Total Steps: " + str(totalSteps)
        # print "Current Heading: " + str(currHeading)
        # distancewalked = (totalSteps * 42) - prevTotalDistance
        Comm.request_data()
        totalSteps = Comm.get_steps()
        currHeading = Comm.get_heading()
        print "Total Steps: " + str(totalSteps)
        print "Current Heading: " + str(currHeading)
        distancewalked = (totalSteps * 42) - prevTotalDistance

        if distancewalked > 0:
            print "distance walked:" + str(distancewalked)
            prevTotalDistance = prevTotalDistance + distancewalked
            print "previous total distance:" + str(prevTotalDistance)
            updateCoordinates(distancewalked, currHeading)
        # Uncomment the code below to key in x and y manually
        # currX = input("Current X: ")
        # currY = input("Current Y: ")
        # currHeading = int(input("Current Heading: "))
        if isAtNextNode(): break;
        giveDirection()
        time.sleep(3)  # delays for 3 seconds
    print "Reached: Node " + str(path[nextNodeIndex] + 1)
    os.system("flite -t 'Reached: Node " + str(path[nextNodeIndex] + 1) + "'")
    nextNodeIndex += 1

print "Reached end node, peace out !"
os.system('flite -t "Reached end node, peace out !" ')

