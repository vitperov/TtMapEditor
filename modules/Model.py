from enum import Enum
from PyQt5.QtCore import *

import json

class HouseSquareType(Enum):
    Empty   = 0
    Corner  = 1
    Wall    = 2
    Door    = 3
    Window  = 4
    Floor   = 5

class HouseSquareRotation(Enum):
    deg0    = 0
    deg90   = 1
    deg180  = 2
    deg270  = 3

class HouseSquareTerritory(Enum):
    Empty       = 0
    Kitchen     = 1
    Bedroom     = 2
    LivingRoom  = 3
    StoreRoom   = 4

class HouseMapSquareModel(QObject):
    changed = pyqtSignal()

    def __init__(self, id):
        QObject.__init__(self)
        self.id = id

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
        self.properties[name] = value;
        self.changed.emit()

    def getProperty(self, name):
        return self.properties[name]

    def toJson(self):
        # properties are enums, they can't be directly converted to int
        props = dict()
        for name, prop in self.properties.items():
            props[name] = prop.value

        props['id'] =  self.id
        return json.dumps(props)
        
    def toSerializableObj(self):
        # properties are enums, they can't be directly converted to int
        obj = dict()
        for name, prop in self.properties.items():
            value = prop
            if not isinstance(value, int):
                value = value.value #FIXME: enum instead
            obj[name] = value

        obj['id'] =  self.id
        return obj
        
    def restoreFromJson(self, js):
        self.id = js['id']
        self.properties['type']      = js['type']
        self.properties['rotation']  = js['rotation']
        self.properties['territory'] = js['territory']


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

