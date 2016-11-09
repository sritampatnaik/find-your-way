from jsonParser import mapParser
import distanceAngleCalculation
import djikstra
import math
import time
import os

### This code is suppossed to be uncommented out in the pi ###
import communication
Comm = communication.Comm()


# Connector nodes between maps
c1L2toC2L2 = 31
c2L2toC2L3 = 16
c2L2toC1L2 = 1
c2L3toC2L2 = 11

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
        os.system("flite -t ' " + turnDirection + str(int(abs(turnAngle))) + " walk " + str(int(round(minDis / 55))) + " steps '")
        print  turnDirection + str(int(abs(turnAngle))) + ' walk ' + str(int(round(minDis/55))) + ' steps  '
    else:
        os.system("flite -t 'Walk straight " + str(int(round(minDis / 55))) + " steps'")
        print 'Walk straight ' + str(int(round(minDis /55))) + ' steps '


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


def setFirstHeading(firstMagReading):
    firstMagReading -= 16
    if firstMagReading < 0:
        firstMagReading += 360
    return firstMagReading

def updateHeading(newMagReading, newGyroReading, oldHeading, oldGyroReading):
    newMagReading -= 16
    if newMagReading < 0 :
        newMagReading += 360

    magDifference = newMagReading - oldHeading
    gyroDifference = newGyroReading - oldGyroReading
    if newMagReading < oldHeading and gyroDifference > 0:
        magDifference += 360
    elif newMagReading > oldHeading and gyroDifference < 0:
        magDifference -= 360

    if abs(gyroDifference) <= 5:
        return oldHeading
    elif abs(gyroDifference) > 5:
        if abs(abs(gyroDifference) - abs(magDifference)) >= 5:
                return int(oldHeading + gyroDifference) % 360
        else:
            return int(newMagReading)


### The following code is for debugging in the ide so comment it in the pi ###
# confirm = ""
# while confirm != "*":
#     startBuildingNo = ""
#     startLevelNo = ""
#     startNodeNo = ""
#     endBuildingNo = ""
#     endLevelNo = ""
#     endNodeNo = ""
#
#     print "Enter starting building number: "
#     while startBuildingNo == "":
#         startBuildingNo = input()
#
#     print startBuildingNo
#
#     print "Starting Level Num: "
#     while startLevelNo == "":
#         startLevelNo = input()
#
#     print startLevelNo
#
#
#     print "Starting Node Num: "
#     while startNodeNo == "":
#         startNodeNo = input()
#
#     print startNodeNo
#
#     print "Enter ending building number: "
#     while endBuildingNo == "":
#         endBuildingNo = input()
#
#     print endBuildingNo
#
#     print "Ending Level Num: "
#     while endLevelNo == "":
#         endLevelNo = input()
#
#     print endLevelNo
#
#     print "Ending Node Num: "
#     while endNodeNo == "":
#         endNodeNo = input()
#
#     print endNodeNo
#
#     confirm = raw_input("confirm:")


### This code is suppossed to be uncommented out in the pi ###
confirm = ""
while confirm != "*":
    startBuildingNo = ""
    startLevelNo = ""
    startNodeNo = ""
    endBuildingNo = ""
    endLevelNo = ""
    endNodeNo = ""

    print "Enter starting building number: "
    os.system('flite -t "Enter starting building number:" ')
    while startBuildingNo == "":
        startBuildingNo = Comm.get_keypad_input()

    print startBuildingNo
    os.system("flite -t 'You entered " + str(startBuildingNo) + "'")

    print "Starting Level Num: "
    os.system('flite -t "Starting Level Num: " ')
    while startLevelNo == "":
        startLevelNo = Comm.get_keypad_input()

    print startLevelNo
    os.system("flite -t 'You entered " + str(startLevelNo) + "'")

    print "Starting Node Num: "
    os.system('flite -t "Starting Node Num:" ')
    while startNodeNo == "":
        startNodeNo = Comm.get_keypad_input()

    print startNodeNo
    os.system("flite -t 'You entered " + str(startNodeNo) + "'")

    print "Enter ending building number: "
    os.system('flite -t "Enter ending building number:" ')
    while endBuildingNo == "":
        endBuildingNo = Comm.get_keypad_input()

    print endBuildingNo
    os.system("flite -t 'You entered " + str(endBuildingNo) + "'")


    print "Ending Level Num: "
    os.system('flite -t "Ending Level Num: " ')
    while endLevelNo == "":
        endLevelNo = Comm.get_keypad_input()

    print endLevelNo
    os.system("flite -t 'You entered " + str(endLevelNo) + "'")

    print "Ending Node Num: "
    os.system('flite -t "Ending Node Num: " ')
    while endNodeNo == "":
        endNodeNo = Comm.get_keypad_input()

    print endNodeNo
    os.system("flite -t 'You entered " + str(endNodeNo) + "'")

    os.system('flite -t "Press star and hash to confirm:" ')
    while confirm == "":
        confirm = Comm.get_keypad_input()

os.system('flite -t "You have confirmed" ')

if int(startBuildingNo) != int(endBuildingNo) and int(startLevelNo) != int(endLevelNo):
    print "here"
    runDjikstra = 3
elif int(startBuildingNo) != int(endBuildingNo) or int(startLevelNo) != int(endLevelNo):
    runDjikstra = 2
else:
    runDjikstra = 1


for y in range(runDjikstra):
    if runDjikstra == 1:
        djikstra.setMap(startBuildingNo, startLevelNo)
        djikstra.dijkstra(int(startNodeNo) - 1)
        path = djikstra.getPath(int(startNodeNo) - 1, int(endNodeNo) - 1)
        currMap = djikstra.getCurrMap()
        reachedEndNodeMsg = "Reached End Node"
    elif runDjikstra == 2:
        if y == 0:
            djikstra.setMap(startBuildingNo, startLevelNo)
            djikstra.dijkstra(int(startNodeNo) - 1)
            if int(startBuildingNo) == 1:
                connectorNode = c1L2toC2L2
                reachedEndNodeMsg = "Reached end of com 1 level 2, Going to com 2 level 2"
            elif int(startLevelNo) == 3:
                connectorNode = c2L3toC2L2
                reachedEndNodeMsg = "Reached end of com 2 level 3, Going to com 2 level 2"
            elif int(startBuildingNo) == 2 and int(endLevelNo) == 3:
                connectorNode = c2L2toC2L3
                reachedEndNodeMsg = "Reached end of com 2 level 2, Going to com 2 level 3"
            elif int(startBuildingNo) == 2 and int(endLevelNo) == 2:
                connectorNode = c2L2toC1L2
                reachedEndNodeMsg = "Reached end of com 2 level 2, Going to com 1 level 2"
            path = djikstra.getPath(int(startNodeNo) - 1, int(connectorNode) - 1)
            currMap = djikstra.getCurrMap()
        elif y == 1:
            djikstra.setMap(endBuildingNo, endLevelNo)
            if int(endBuildingNo) == 1:
                connectorNode = c1L2toC2L2
            elif int(endLevelNo) == 3:
                connectorNode = c2L3toC2L2
            elif int(endBuildingNo) == 2 and int(startLevelNo) == 3:
                connectorNode = c2L2toC2L3
            elif int(endBuildingNo) == 2 and int(startLevelNo) == 2:
                connectorNode = c2L2toC1L2
            print connectorNode
            djikstra.dijkstra(int(connectorNode) - 1)
            path = djikstra.getPath(int(connectorNode) - 1, int(endNodeNo) - 1)
            currMap = djikstra.getCurrMap()
            reachedEndNodeMsg = "Reached End Node"
    elif runDjikstra == 3:
        if y == 0:
            djikstra.setMap(startBuildingNo, startLevelNo)
            djikstra.dijkstra(int(startNodeNo) - 1)
            if int(startBuildingNo) == 1:
                connectorNode = c1L2toC2L2
                reachedEndNodeMsg = "Reached end of com 1 level 2, Going to com 2 level 2"
            elif int(startLevelNo) == 3:
                connectorNode = c2L3toC2L2
                reachedEndNodeMsg = "Reached end of com 2 level 3, Going to com 2 level 2"
            elif int(startBuildingNo) == 2 and int(endLevelNo) == 3:
                connectorNode = c2L2toC2L3
                reachedEndNodeMsg = "Reached end of com 2 level 2, Going to com 2 level 3"
            elif int(startBuildingNo) == 2 and int(endLevelNo) == 2:
                connectorNode = c2L2toC1L2
                reachedEndNodeMsg = "Reached end of com 2 level 2, Going to com 1 level 2"
            path = djikstra.getPath(int(startNodeNo) - 1, int(connectorNode) - 1)
            currMap = djikstra.getCurrMap()
        elif y == 1:
            djikstra.setMap(2, 2)
            if int(startBuildingNo) == 1:
                djikstra.dijkstra(int(c2L2toC1L2) - 1)
                path = djikstra.getPath(int(c2L2toC1L2) - 1, int(c2L2toC2L3) - 1)
                currMap = djikstra.getCurrMap()
                reachedEndNodeMsg = "Reached end of com 2 level 2, Going to com 2 level 3"
            elif int(startLevelNo) == 3:
                djikstra.dijkstra(int(c2L2toC2L3) - 1)
                path = djikstra.getPath(int(c2L2toC2L3) - 1, int(c2L2toC1L2) - 1)
                currMap = djikstra.getCurrMap()
                reachedEndNodeMsg = "Reached end of com 2 level 2, Going to com 1 level 2"
        elif y == 2:
            djikstra.setMap(endBuildingNo, endLevelNo)
            if int(endBuildingNo) == 1:
                connectorNode = c1L2toC2L2
            elif int(endLevelNo) == 3:
                connectorNode = c2L3toC2L2
            elif int(endBuildingNo) == 2 and int(startLevelNo) == 3:
                connectorNode = c2L2toC2L3
            elif int(endBuildingNo) == 2 and int(startLevelNo) == 2:
                connectorNode = c2L2toC1L2
            print connectorNode
            djikstra.dijkstra(int(connectorNode) - 1)
            path = djikstra.getPath(int(connectorNode) - 1, int(endNodeNo) - 1)
            currMap = djikstra.getCurrMap()
            reachedEndNodeMsg = "Reached end node, peace out !"

    print "Path:",  # path
    for x in range(len(path)):
        print path[x] + 1,

    nextNodeIndex = 1
    currX = int(currMap.buildingMap['map'][path[0]]['x'])
    currY = int(currMap.buildingMap['map'][path[0]]['y'])
    prevTotalDistance = 0

    ### The following code is for debugging in the ide so comment it in the pi ###
    # firstMagReading = input("Heading:" )
    # firstGyroReading = input("Gyro:")
    # currHeading = setFirstHeading(firstMagReading)
    # oldGyroReading = firstGyroReading
    # giveDirection()
    # steps = 0

    ### This code is suppossed to be uncommented out in the pi ###
    Comm.request_data()
    firstMagReading = Comm.get_heading()
    firstGyroReading = Comm.get_gyro()
    currHeading = setFirstHeading(firstMagReading)
    oldGyroReading = firstGyroReading
    giveDirection()
    steps = 0

    while (nextNodeIndex != len(path)):
        while not (isAtNextNode()):
            ### The following code is for debugging in the ide so comment it in the pi ###
            # stepStatus = input("Steps walked: ")
            # newMagReading = input("Heading:")
            # newGyroReading = input("Gyro:")
            # currHeading = updateHeading(newMagReading, newGyroReading, currHeading, oldGyroReading)
            # oldGyroReading = newGyroReading
            # print "Step Status: " + str(stepStatus)
            # print "Current Heading: " + str(currHeading)
            # distancewalked = 55

            ### This code is suppossed to be uncommented out in the pi ###
            Comm.request_data()
            stepStatus = Comm.get_steps()
            newMagReading = Comm.get_heading()
            newGyroReading = Comm.get_gyro()
            currHeading = updateHeading(newMagReading, newGyroReading, currHeading, oldGyroReading)
            oldGyroReading = newGyroReading
            print "Step Status: " + str(stepStatus)
            print "Current Heading: " + str(currHeading)


            if stepStatus > steps:
                distancewalked = 55*(stepStatus-steps)
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
        os.system("flite -t 'Reached: Node " + str(path[nextNodeIndex] + 1) + "'")
        nextNodeIndex += 1

    print reachedEndNodeMsg
    os.system("flite -t '" + reachedEndNodeMsg + "'")

