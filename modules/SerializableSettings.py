import json
from json import JSONEncoder
from abc import ABC, abstractmethod

# Derive from AbstractBaseClass to have abstract method
#   that must be redifined in a child class
class SerializableSettings(ABC):
    class SettingsEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
        
    def __init__(self, filename):
        # This varible shouldn't be written to json, but I don't
        #   know how to hide it from json.dumps
        self._filename = filename

    def saveToFile(self):
        print("Saving data to " + self._filename)
        with open(self._filename, "w+") as writeFile:
            jsonObj = json.dumps(self, indent=4, cls=self.SettingsEncoder)
            writeFile.write(jsonObj)

    def loadFromFile(self):
        print("Loading data from " + self._filename)

        with open(self._filename, "r") as readFile:
            jsStr = readFile.read()
            settingsDict = json.loads(jsStr)
            self.loadFromDict(settingsDict)

    @abstractmethod
    def loadFromDict(self):
        pass


