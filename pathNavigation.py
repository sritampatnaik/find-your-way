from jsonParser import mapParser
import distanceAngleCalculation
import djikstra
import math
import time
import os

### This code is suppossed to be uncommented out in the pi ###
# import communication
# Comm = communication.Comm()


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
        # os.system("flite -t ' " + turnDirection + str(int(abs(turnAngle))) + " walk " + str(int(round(minDis / 42))) + " steps '")
        print  turnDirection + str(int(abs(turnAngle))) + ' walk ' + str(int(round(minDis/42))) + ' cms  '
    else:
        # os.system("flite -t 'Walk straight " + str(int(round(minDis / 42))) + " steps'")
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


def updateHeading(heading):
    heading = heading - 16
    if(heading<0):
        heading=heading+360
    return heading


### The following code is for debugging in the ide so comment it in the pi ###
startingNode = ""
endingNode = ""
print "Enter starting node "
while (startingNode == ""):
    startingNode = input()

print startingNode

print "Enter ending Node: "
while (endingNode == ""):
    endingNode = input()

print endingNode

### This code is suppossed to be uncommented out in the pi ###
# startingNode = ""
# endingNode = ""
# os.system('flite -t "Enter starting node" ')
# print "Enter starting node "
# while (startingNode == ""):
#     startingNode = Comm.get_keypad_input()
#
# os.system("flite -t 'You entered " + str(startingNode) + "'")
# print startingNode
#
# os.system('flite -t "Enter ending node" ')
# print "Enter ending Node: "
# while (endingNode == ""):
#     endingNode = Comm.get_keypad_input()
#
# os.system("flite -t 'You entered " + str(endingNode) + "'")
# print endingNode


djikstra.dijkstra(int(startingNode) - 1)
path = djikstra.getPath(int(startingNode) - 1, int(endingNode) - 1)
currMap = djikstra.getCurrMap()
print "Path:",  # path
for x in range(len(path)):
    print path[x] + 1,

nextNodeIndex = 1
currX = int(currMap.buildingMap['map'][path[0]]['x'])
currY = int(currMap.buildingMap['map'][path[0]]['y'])
prevTotalDistance = 0

### The following code is for debugging in the ide so comment it in the pi ###
currHeading =updateHeading(input("Heading:" ))
giveDirection()
steps = 0

### This code is suppossed to be uncommented out in the pi ###
# Comm.request_data()
# currHeading =updateHeading( Comm.get_heading() )
# giveDirection()
# steps = 0

while (nextNodeIndex != len(path)):
    while not (isAtNextNode()):
        ### The following code is for debugging in the ide so comment it in the pi ###
        stepStatus = input("stepStatus")
        currHeading = updateHeading(input("Heading:"))
        print "Step Status: " + str(stepStatus)
        print "Current Heading: " + str(currHeading)
        distancewalked = 42

        ### This code is suppossed to be uncommented out in the pi ###
        # Comm.request_data()
        # stepStatus = Comm.get_steps()
        # currHeading = updateHeading(Comm.get_heading())
        # print "Step Status: " + str(stepStatus)
        # print "Current Heading: " + str(currHeading)
        # distancewalked = 42

        if stepStatus > steps:
            prevTotalDistance = prevTotalDistance + distancewalked
            print "previous total distance:" + str(prevTotalDistance)
            steps = stepStatus
            updateCoordinates(distancewalked, currHeading)

        # Uncomment the code below to key in x and y manually
        # currX = input("Current X: ")
        # currY = input("Current Y: ")
        # currHeading = int(input("Current Heading: "))
        if isAtNextNode(): break;
        giveDirection()
        # time.sleep(1)
	# delays for 1 seconds
    print "Reached: Node " + str(path[nextNodeIndex] + 1)
    # os.system("flite -t 'Reached: Node " + str(path[nextNodeIndex] + 1) + "'")
    nextNodeIndex += 1

print "Reached end node, peace out !"
# os.system('flite -t "Reached end node, peace out !" ')

