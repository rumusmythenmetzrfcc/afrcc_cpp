
import json

def loadJsonData(path):
  with open(path) as stream:
    return json.load(stream)