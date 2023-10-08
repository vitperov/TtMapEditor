import json
from json import JSONEncoder

class DictLoadableObject():
    def loadFromDict(self, settings):
        for k, v in settings.items():
            storedVal = getattr(self, k)

            if hasattr(storedVal, 'loadFromDict') and callable(storedVal.loadFromDict):
                valClass = type(storedVal)
                newObj = valClass()
                newObj.loadFromDict(v)
                setattr(self, k, newObj)
            elif isinstance(storedVal, list):
                newList = list()
                # NOTE: it must be at least one empty object in the list
                # to determine type of it.
                ItemClass = type(storedVal[0])
                for item in v:
                    a = ItemClass()
                    a.loadFromDict(item)
                    newList.append(a)
                lastItem = newList[-1]
                if len(lastItem.name): #FIXME: add method .isEmpty()
                    # Insert one empty value to be able to
                    # 1) determine type of it (see above)
                    # 2) It's used in an editor to create new item
                    #      in the list.
                    newList.append(ItemClass())

                setattr(self, k, newList)
            else:
                setattr(self, k, v)

class SerializableSettings(DictLoadableObject):
    class SettingsEncoder(JSONEncoder):
        def default(self, o):
            d = dict(o.__dict__) # copy because we delete items
            keysToDelete = ['_filename']

            # FIXME: delete all private keys
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

