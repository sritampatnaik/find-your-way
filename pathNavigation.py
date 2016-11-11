from jsonParser import mapParser
import distanceAngleCalculation
import djikstra
import math
import time
import os

### This code is suppossed to be uncommented out in the pi ###
# import communication
# Comm = communication.Comm()


# Connector nodes between maps
c1L2toC2L2 = 31
c2L2toC2L3 = 16
c2L2toC1L2 = 1
c2L3toC2L2 = 11

# Step variable
stepLength = 47

# Corridor Array
c1L2 = [0]*41
c1L2[32]= 1
c1L2[39]= 1
c1L2[17]= 1
c1L2[21]= 1
c1L2[24]= 1
c1L2[18]= 1
c1L2[22]= 1
c1L2[34]= 1
c1L2[26]= 1
c1L2[29]= 1
c1L2[31]= 1
c1L2[28] = 1
c1L2[1] = 1
c1L2[2] = 1

c2L2 = [0]*21
c2L2[1] = 1
c2L2[17] = 1
c2L2[2] = 1
c2L2[5] = 1
c2L2[19] = 1
c2L2[11] = 1
c2L2[12] = 1
c2L2[7] = 1
c2L2[8] = 1
c2L2[10] = 1
c2L2[6] = 1
c2L2[13] = 1
c2L2[14] = 1
c2L2[15] = 1
c2L2[16] = 1

c2L3 = [0]*17
c2L3[1] = 1
c2L3[16] = 1
c2L3[2] = 1
c2L3[7] = 1
c2L3[8] = 1
c2L3[3] = 1
c2L3[4] = 1
c2L3[12] = 1
c2L3[6] = 1
c2L3[10] = 1
c2L3[11] = 1
c2L3[9] = 1

feedbackFlag = 0
straightFlag = 0
currAngle = 0
warnFlag = 0

def giveWarning(currNode, nextNode, disLeft, bnum, lnum):
    global warnFlag
    if bnum == 1 and lnum == 2:
        if currNode == 34 and nextNode == 26:
            if disLeft <= 250:
                # os.system("flite -t 'Vaani bang bang ahead '")
                print "glass hai aage"
                warnFlag = 1
        elif currNode == 26 and nextNode == 29:
            # os.system("flite -t 'Vaani bang bang ahead  '")
            print "glass hai aage"
            warnFlag = 1
        elif currNode == 29 and nextNode == 26:
            if disLeft <= 250:
                # os.system("flite -t 'Vaani bang bang ahead  '")
                print "glass hai aage"
                warnFlag = 1
        elif currNode == 15 and nextNode == 32:
            # os.system("flite -t 'Vaani bang bang ahead  '")
            print "glass hai aage"
            warnFlag = 1
        elif currNode == 32 and nextNode == 15:
            # os.system("flite -t 'Vaani bang bang ahead  '")
            print "glass hai aage"
            warnFlag = 1
    elif bnum == 2 and lnum == 2:
        if currNode == 6 and nextNode == 11:
            if disLeft <= 250:
                # os.system("flite -t 'Vaani bang bang ahead  '")
                print "glass hai aage"
                warnFlag = 1
        elif currNode == 11 and nextNode == 12:
            if disLeft <= 250:
                # os.system("flite -t 'Vaani bang bang ahead  '") #wooden door
                print "wood hai aage"
                warnFlag = 1
        elif currNode == 12 and nextNode == 13:
            if disLeft <= 250:
                # os.system("flite -t 'Vaani bang bang ahead  '") #wooden door
                print "wood hai aage"
                warnFlag = 1
        elif currNode == 14 and nextNode == 15:
            # os.system("flite -t 'Stairs Ahead'")
            print "stair hai aage"
            warnFlag = 1
    elif bnum == 2 and lnum == 3:
        if currNode == 8 and nextNode == 7:
            if disLeft <= 250:
                # os.system("flite -t 'Glass door approaching '")
                print "glass hai aage"
                warnFlag = 1
        elif currNode == 9 and nextNode == 8:
            if disLeft <= 250:
                # os.system("flite -t 'Wooden door approaching '")
                print "wood hai aage"
                warnFlag = 1
        elif currNode == 10 and nextNode == 9:
            # os.system("flite -t 'Wooden door approaching '")
            print "wood hai aage"
            warnFlag = 1
        elif currNode == 11 and nextNode == 10:
            # os.system("flite -t 'Stairs Ahead'")
            print "stair hai aage"
            warnFlag = 1

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
    if straightFlag == 1:
        # os.system("flite -t 'Walk straight " + str(int(round(minDis / stepLength))) + " steps'")
        print 'Walk straight ' + str(int(round(minDis / stepLength))) + ' steps '
    else:
        if (currAngle - currHeading) < -180:
            turnAngle = (currAngle - currHeading) + 360
        else:
            turnAngle = currAngle - currHeading

        if turnAngle < 0:
            turnDirection = 'left'
        else:
            turnDirection = 'right'

        if abs(turnAngle) > 10:
            # os.system("flite -t ' " + turnDirection + str(int(abs(turnAngle))) + " walk " + str(int(round(minDis / stepLength))) + " steps '")
            print  turnDirection + str(int(abs(turnAngle))) + ' walk ' + str(int(round(minDis/stepLength))) + ' steps  '

        else:
            # os.system("flite -t 'Walk straight " + str(int(round(minDis / stepLength))) + " steps'")
            print 'Walk straight ' + str(int(round(minDis /stepLength))) + ' steps '

def isAtNextNode():
    disToNextNode = distanceAngleCalculation.distance(currX, currY,
                                                      currMap.buildingMap['map'][path[nextNodeIndex]]['x'],
                                                      currMap.buildingMap['map'][path[nextNodeIndex]]['y'])
    if disToNextNode < 51:
        return True
    return False

def updateCoordinates(distanceWalked, newHeading):
    global currX
    global currY
    # calculate angle of triangle
    alpha = 360 - int(currMap.buildingMap['info']['northAt']) + 90
    if alpha > 429:
            alpha = alpha - 360
    theta = newHeading - alpha

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

def updateHeading(firstMagReading):
    firstMagReading -= 16
    if firstMagReading < 0:
        firstMagReading += 360
    return firstMagReading

def getTurnAngle(idealHead, magReading):
    if (idealHead - magReading) < -180:
        return (idealHead - magReading) + 360
    else:
        return idealHead - magReading

def checkCorridor(map):
    if map.buildingName == 1 and map.levelNo == 2:
        return c1L2[path[nextNodeIndex - 1] + 1] == 1 and c1L2[path[nextNodeIndex] + 1] == 1
    elif map.buildingName == 2 and map.levelNo == 2:
        return c2L2[path[nextNodeIndex - 1] + 1] == 1 and c2L2[path[nextNodeIndex] + 1] == 1
    elif map.buildingName == 2 and map.levelNo == 3:
        return c2L3[path[nextNodeIndex - 1] + 1] == 1 and c2L3[path[nextNodeIndex] + 1] == 1

### The following code is for debugging in the ide so comment it in the pi ###
confirm = ""
while confirm != "*":
    startBuildingNo = ""
    startLevelNo = ""
    startNodeNo = ""
    endBuildingNo = ""
    endLevelNo = ""
    endNodeNo = ""

    print "Enter starting building number: "
    while startBuildingNo == "":
        startBuildingNo = input()

    print "Starting Level Num: "
    while startLevelNo == "":
        startLevelNo = input()

    print "Starting Node Num: "
    while startNodeNo == "":
        startNodeNo = input()

    print "Enter ending building number: "
    while endBuildingNo == "":
        endBuildingNo = input()

    print "Ending Level Num: "
    while endLevelNo == "":
        endLevelNo = input()

    print "Ending Node Num: "
    while endNodeNo == "":
        endNodeNo = input()

    confirm = raw_input("confirm:")

### This code is suppossed to be uncommented out in the pi ###
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
#     os.system('flite -t "Enter starting building number:" ')
#     while startBuildingNo == "":
#         startBuildingNo = Comm.get_keypad_input()
#
#     print startBuildingNo
#     os.system("flite -t 'You entered " + str(startBuildingNo) + "'")
#
#     print "Starting Level Num: "
#     os.system('flite -t "Starting Level Num: " ')
#     while startLevelNo == "":
#         startLevelNo = Comm.get_keypad_input()
#
#     print startLevelNo
#     os.system("flite -t 'You entered " + str(startLevelNo) + "'")
#
#     print "Starting Node Num: "
#     os.system('flite -t "Starting Node Num:" ')
#     while startNodeNo == "":
#         startNodeNo = Comm.get_keypad_input()
#
#     print startNodeNo
#     os.system("flite -t 'You entered " + str(startNodeNo) + "'")
#
#     print "Enter ending building number: "
#     os.system('flite -t "Enter ending building number:" ')
#     while endBuildingNo == "":
#         endBuildingNo = Comm.get_keypad_input()
#
#     print endBuildingNo
#     os.system("flite -t 'You entered " + str(endBuildingNo) + "'")
#
#
#     print "Ending Level Num: "
#     os.system('flite -t "Ending Level Num: " ')
#     while endLevelNo == "":
#         endLevelNo = Comm.get_keypad_input()
#
#     print endLevelNo
#     os.system("flite -t 'You entered " + str(endLevelNo) + "'")
#
#     print "Ending Node Num: "
#     os.system('flite -t "Ending Node Num: " ')
#     while endNodeNo == "":
#         endNodeNo = Comm.get_keypad_input()
#
#     print endNodeNo
#     os.system("flite -t 'You entered " + str(endNodeNo) + "'")
#
#     os.system('flite -t "Press star and hash to confirm:" ')
#     while confirm == "":
#         confirm = Comm.get_keypad_input()
#
# os.system('flite -t "You have confirmed" ')

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
    stepStatus = 0
    magReading = input("Heading:" )
    currHeading = updateHeading(magReading)
    steps = 0

    ### This code is suppossed to be uncommented out in the pi ###
    # Comm.request_data()
    # time.sleep(1)
    # Comm.request_data()
    # magReading = Comm.get_heading()
    # currHeading = updateHeading(magReading)
    # Comm.send_reset()
    # stepStatus = 0
    # steps = 0

    while (nextNodeIndex != len(path)):
        straightFlag = 0
        isCorridor = False
        warnFlag = 0
        while not (isAtNextNode()):
            idealHeading = distanceAngleCalculation.calcAngle(int(currMap.buildingMap['map'][path[nextNodeIndex - 1]]['x']),
                                                        int(currMap.buildingMap['map'][path[nextNodeIndex - 1]]['y']),
                                                        int(currMap.buildingMap['map'][path[nextNodeIndex]]['x']),
                                                        int(currMap.buildingMap['map'][path[nextNodeIndex]]['y']),
                                                        int(currMap.buildingMap['info']['northAt']))


            isCorridor = checkCorridor(currMap)

            if isCorridor and straightFlag == 0:
                print "Bloop:"
                print isCorridor
                while abs(getTurnAngle(idealHeading, currHeading)) >= 10:
                    ### The following code is for debugging in the ide so comment it in the pi ##
                    stepStatus = input("Stray steps: ")
                    magReading = input("Heading: ")
                    currHeading = updateHeading(magReading)
                    steps = stepStatus

                    ### This code is suppossed to be uncommented out in the pi ###
                    # Comm.request_data()
                    # stepStatus = Comm.get_steps()
                    # magReading = Comm.get_heading()
                    # currHeading = updateHeading(magReading)
                    # steps = stepStatus

                    giveDirection()
                straightFlag = 1


            ### The following code is for debugging in the ide so comment it in the pi ###
            stepStatus = input("Steps walked: ")
            magReading = input("Heading: ")
            currHeading = updateHeading(magReading)
            print "Step Status: " + str(stepStatus)
            print "Current Heading: " + str(currHeading)
            distancewalked = stepLength

            ### This code is suppossed to be uncommented out in the pi ###
            # Comm.request_data()
            # stepStatus = Comm.get_steps()
            # magReading = Comm.get_heading()
            # currHeading = updateHeading(magReading)
            # print "Step Status: " + str(stepStatus)
            # print "Current Heading: " + str(currHeading)
            # print path[nextNodeIndex-1] + 1
            # print path[nextNodeIndex] + 1

            if stepStatus > steps:
                disleft = distanceAngleCalculation.distance(currX, currY,
                                                            currMap.buildingMap['map'][path[nextNodeIndex]]['x'],
                                                            currMap.buildingMap['map'][path[nextNodeIndex]]['y'])
                distancewalked = stepLength * (stepStatus - steps)
                if straightFlag == 1 and distancewalked > disleft:
                    distancewalked = disleft
                steps = stepStatus
                if straightFlag == 1:
                    idealHeadingNew = idealHeading
                    if idealHeading < 0:
                        idealHeadingNew += 360
                    print "Ideal heading: " + str(idealHeadingNew)
                    updateCoordinates(distancewalked, idealHeadingNew)
                else:
                    updateCoordinates(distancewalked, currHeading)

            # Uncomment the code below to key in x and y manually
            # currX = input("Current X: ")
            # currY = input("Current Y: ")
            # currHeading = int(input("Current Heading: "))

            if isAtNextNode(): break;
            giveDirection()
            if warnFlag == 0:
                disleft = distanceAngleCalculation.distance(currX, currY,
                                                           currMap.buildingMap['map'][path[nextNodeIndex]]['x'],
                                                           currMap.buildingMap['map'][path[nextNodeIndex]]['y'])
                print "Dis Left: " + str(disleft)
                print str(path[nextNodeIndex - 1] + 1)
                print str(path[nextNodeIndex ] + 1)
                giveWarning(path[nextNodeIndex - 1] + 1, path[nextNodeIndex] + 1, disleft, currMap.buildingName, currMap.levelNo)
            # time.sleep(1)
        # delays for 1 seconds

        print "Reached: Node " + str(path[nextNodeIndex] + 1)
        # os.system("flite -t 'Reached: Node " + str(path[nextNodeIndex] + 1) + "'")
        nextNodeIndex += 1

    print reachedEndNodeMsg
    # os.system("flite -t '" + reachedEndNodeMsg + "'")

