import json
from json import JSONEncoder
from abc import ABC, abstractmethod

# Derive from AbstractBaseClass to have abstract method
#   that must be redifined in a child class
class SerializableSettings(ABC):
    class SettingsEncoder(JSONEncoder):
        def default(self, o):
            d = dict(o.__dict__) # copy because we delete items
            keysToDelete = ['_filename', '_abc_impl']

            for key in keysToDelete:
                d.pop(key, None)

            return d;

    def __init__(self, filename):
        self._filename = filename

    def saveToFile(self):
        print("Saving data to " + self._filename)
        with open(self._filename, "w+") as writeFile:
            jsonObj = json.dumps(self, indent=4, cls=self.SettingsEncoder)
            jsonObj
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


