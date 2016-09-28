import urllib, json, jsonParser, djikstra
url = "http://ShowMyWay.comp.nus.edu.sg/getMapInfo.php?Building=COM1&Level=2"
response = urllib.urlopen(url)
data = json.loads(response.read())
# print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
# print djikstra.getPath(1,2)