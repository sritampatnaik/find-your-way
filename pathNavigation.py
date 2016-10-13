from jsonParser import mapParser
import distanceAngleCalculation
import djikstra
import math

startingNode = input("Starting Node: ")
endingNode = input("Ending Node: ")
djikstra.dijkstra(startingNode - 1)
path = djikstra.getPath(startingNode - 1, endingNode - 1)
print "Path:",  # path
for x in range(len(path)):
    print path[x] + 1,
