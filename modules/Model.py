from enum import Enum
from PyQt5.QtCore import *

import json

class HouseSquareType(str, Enum):
    Empty   = 'Empty'
    Corner  = 'Corner'
    Wall    = 'Wall'
    Door    = 'Door'
    Window  = 'Window'
    Floor   = 'Floor'

class HouseSquareRotation(str, Enum):
    deg0    = '0'
    deg90   = '90'
    deg180  = '180'
    deg270  = '270'

class HouseSquareTerritory(str, Enum):
    Empty       = 'Empty'
    Kitchen     = 'Kitchen'
    Bedroom     = 'Bedroom'
    LivingRoom  = 'LivingRoom'
    StoreRoom   = 'StoreRoom'

class HouseMapSquareModel(QObject):
    changed = pyqtSignal()

    def __init__(self, id):
        QObject.__init__(self)
        self.id = id

        self.classnames = dict()
        self.classnames['type']      = HouseSquareType
        self.classnames['rotation']  = HouseSquareRotation
        self.classnames['territory'] = HouseSquareTerritory

        self.properties = dict()
        self.properties['type']      = HouseSquareType.Empty
        self.properties['rotation']  = HouseSquareRotation.deg0
        self.properties['territory'] = HouseSquareTerritory.Empty

    def getXY(self):
        y = int(self.id / 1000)
        x = self.id % 1000

        return [x, y]

    def setProperty(self, name, value):
        print("setProperty " + name + ": " + str(value))
        variableClass = self.classnames[name]
        self.properties[name] = variableClass(value);
        self.changed.emit()

    def getProperty(self, name):
        return self.properties[name]

    def toSerializableObj(self):
        # properties are enums, they can't be directly converted to int
        obj = dict()
        for name, prop in self.properties.items():
            value = prop
            obj[name] = value

        obj['id'] =  self.id
        return obj

    def restoreFromJson(self, js):
        self.id = js['id']
        self.properties['type']      = HouseSquareType(js['type'])
        self.properties['rotation']  = HouseSquareRotation(js['rotation'])
        self.properties['territory'] = HouseSquareTerritory(js['territory'])


class HouseMapModel(QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self):
        QObject.__init__(self)

        self.width = 0
        self.height = 0
        self._squares = dict()

    def newMap(self, h, w):
        self.width = w
        self.height = h
        for row in range(h):
            for column in range(w):
                id = row*1000 + column
                self._squares[id] = HouseMapSquareModel(id)

        self.updatedEntireMap.emit()

    def getSquare(self, id):
        return self._squares[id]

    def getAllSquares(self):
        return self._squares

    def size(self):
        return [self.height, self.width]

    def toSerializableObj(self):
        squares = dict()
        for id, square in self._squares.items():
            squares[id] = square.toSerializableObj()

        obj = dict()
        obj['version'] = 1
        obj['squares'] = squares
        obj['width']   = self.width
        obj['height']  = self.height

        return obj

    def restoreFromJson(self, js):
        self.width  = js['width']
        self.height = js['height']

        self._squares = dict()
        for id, square in js['squares'].items():
            id = int(id)
            obj = HouseMapSquareModel(id)
            obj.restoreFromJson(square)
            self._squares[id] = obj

    def saveMap(self, filename):
        extension = '.house'
        if not filename.endswith(extension):
            filename = filename + extension

        print("Saving map to " + filename)
        with open(filename, "w") as writeFile:
            json.dump(self.toSerializableObj(), writeFile, indent=4)

    def openMap(self, filename):
        extension = '.house'
        if not filename.endswith(extension):
            filename = filename + extension

        print("Loading map to " + filename)

        with open(filename, "r") as readFile:
            jsObj = json.load(readFile)
            self.restoreFromJson(jsObj)

        self.updatedEntireMap.emit()

