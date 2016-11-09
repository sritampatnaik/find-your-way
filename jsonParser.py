import json
import urllib2
import distanceAngleCalculation

# This program retrieves the map of the building (com1L2, com2L2, com2L3) in json format
# It then stores the in an adjacency matrix the following info:
# in top right half, distance in cm between nodes in adjacency matrix
# in bottom left half, angle between nodes
# angle always is calculated from the smaller index to the larger index
# negative angle means turn left, positive means right

# METHODS SUPPORTED
# getLocationName(index)
# def getLocationXCoord(index)
# def getLocationYCoord(index)
# getAngle(point1, point2)
# getDistance(point1, point2)

class mapParser(object):
    #self is a reference to the current instance of the class other language pass it implicitly but not in python
    def __init__(self, buildingName, levelNo):
        self.buildingName = buildingName #saving building name basically whatever you passed as the param to mapParser
        self.levelNo = levelNo #saving leve no basically whatever you passed as the second param to mapParser
        self.buildingMap = {} #empty building dictionary
        self.northAt = 0
        self.numElements = 0
        self.matrix = {}
        self.loadMap(buildingName, levelNo)
        self.fillAMatrix()

    #returns the URL of the map
    def mapUrl(self, identifier):
        map = {"com1L2": "http://ShowMyWay.comp.nus.edu.sg/getMapInfo.php?Building=COM1&Level=2",
               "com2L2": "http://showmyway.comp.nus.edu.sg/getMapInfo.php?Building=COM2&Level=2",
               "com2L3": "http://showmyway.comp.nus.edu.sg/getMapInfo.php?Building=COM2&Level=3"}
        return map[identifier]

    def loadMap(self, buildingName, levelNo):
        try:
            jsonMap = urllib2.urlopen("http://ShowMyWay.comp.nus.edu.sg/getMapInfo.php?Building=" + str(buildingName) + "&Level=" + str(levelNo))
            self.buildingMap = json.load(jsonMap)
        except:
            with open('maps/COM' + str(buildingName) + 'L' + str(levelNo) +'.json') as json_data:
                self.buildingMap = json.load(json_data)
        self.northAt = int(self.buildingMap['info']['northAt'])
        self.numElements = len(self.buildingMap.get('map'))
        self.matrix = [[0] * self.numElements for i in range(self.numElements)]

    def fillAMatrix(self):
        # in top right half, store distance in cm between nodes in adjacency matrix
        # in bottom left half, store angle between nodes
        # angle always is calculated from the smaller index to the larger index
        # negative angle means turn left, positive means right
        for i in range(self.numElements):
            self.linkString = self.buildingMap['map'][i]['linkTo']
            self.linkArray = [int(s) for s in self.linkString.split(',')]
            x1 = int(self.buildingMap['map'][i]['x'])
            y1 = int(self.buildingMap['map'][i]['y'])
            for j in self.linkArray:
                x2 = int(self.buildingMap['map'][j - 1]['x'])
                y2 = int(self.buildingMap['map'][j - 1]['y'])
                if self.matrix[j - 1][i] == 0:
                    self.matrix[i][j - 1] = distanceAngleCalculation.distance(
                        x1, y1, x2, y2)
                else:
                    self.matrix[i][j - 1] = distanceAngleCalculation.calcAngle(
                        x2, y2, x1, y1, self.northAt)

    # returns the name of the location at the index
    def getLocationName(self, index):
        return self.buildingMap['map'][index]['nodeName']

    # returns the x-coordinate of the location at the index
    def getLocationXCoord(self, index):
        return self.buildingMap['map'][index]['x']

    # returns the y-coordinate of the location at the index
    def getLocationYCoord(self, index):
        return self.buildingMap['map'][index]['y']

    # returns the angle between 2 points
    def getAngle(self, point1, point2):
        if point1 < point2:
            return self.matrix[point2][point1]
        else:
            return (self.matrix[point1][point2] + 180)

    # returns the distance between 2 locations
    def getDistance(self, point1, point2):
        if point1 < point2:
            return self.matrix[point1][point2]
        else:
            return self.matrix[point2][point1]

    def printMap(self):
        print('\n'.join([' '.join(['{:5}'.format(item) for item in row[0:15]])
                         for row in self.matrix[0:15]]))


        # EXTRA STUFF FOR TESTING AND PRINTING#

        # print json.dumps(buildingMap.get('map'), indent=4)
        # print json.dumps(com1L2Map, indent=4)
        # print com1L2Map.get('info').get('northAt')

        # testjson = json.dumps({"info": {
        #	    "northAt": "315"
        #	},
        #	"map": [
        #        {
        #            "y": "2436",
        #           "x": "0",
        #          "nodeId": "1",
        #            "linkTo": "2",
        #            "nodeName": "TO LT15"
        #        },
        #        {
        #            "y": "2436",
        #            "x": "2152",
        #            "nodeId": "2",
        #            "linkTo": "1, 3, 4  ",
        #            "nodeName": "P2"
        #        },
        #        {
        #            "y": "731",
        #            "x": "2152",
        #            "nodeId": "3",
        #             "linkTo": "2",
        #            "nodeName": "Linkway"
        #        },
        #        {
        #            "y": "2436",
        #            "x": "2883",
        #            "nodeId": "4",
        #            "linkTo": "2",
        #            "nodeName": "P4"
        #        }
        #	]})

