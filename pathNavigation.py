from jsonParser import mapParser
import distanceAngleCalculation
import djikstra
import math

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

# def updateCoordinates(distanceWalked, heading):
#     # calculate angle of triangle
#     theta = heading - currHeading
#
#     # take abs values in case angle is not acute. walker is a cock.
#     deltaX = math.fabs(distanceWalked * math.sin(math.rad(theta)))
#     deltaY = math.fabs(distanceWalked * math.cos(math.rad(theta)))
#
#     # update coordinates
#     if 0 < theta <= 90:
#         currX = deltaX + currX
#         currY += deltaY
#     elif 90 < theta <= 180:
#         currX -= deltaX
#         currY += deltaY
#     elif 180 < theta <= 270:
#         currX -= deltaX
#         currY -= deltaY
#     # 270 < theta <= 360 is assumed here
#     else:
#         currX += deltaX
#         currY -= deltaY

startingNode = input("Starting Node: ")
endingNode = input("Ending Node: ")
djikstra.dijkstra(startingNode - 1)
path = djikstra.getPath(startingNode - 1, endingNode - 1)
currMap = djikstra.getCurrMap()
print "Path:",  # path
for x in range(len(path)):
    print path[x] + 1,

nextNodeIndex = 1
currX = currMap.buildingMap['map'][path[0]]['x']
currY = currMap.buildingMap['map'][path[0]]['y']
currHeading = currMap.buildingMap['info']['northAt']

while (nextNodeIndex != len(path)):
    while not (isAtNextNode()):
        currX = input("Current X: ")
        currY = input("Current Y: ")
        currHeading = int(input("Current Heading: "))
        if isAtNextNode(): break;
        giveDirection()
    print "Reached: Node " + str(path[nextNodeIndex])
    nextNodeIndex += 1

