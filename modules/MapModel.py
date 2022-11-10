from enum import Enum
from PyQt5.QtCore import *

import json

class SquareType(str, Enum):
    Empty   = 'Empty'
    Grass   = 'Grass'
    Forest  = 'Forest'
    Road    = 'Road'
    House   = 'House'
    Shed    = 'Shed'

class MapSquareModel(QObject):
    changed = pyqtSignal()

    def __init__(self, id):
        QObject.__init__(self)
        self.id = id

        self.classnames = dict()
        self.classnames['type']      = SquareType

        self.properties = dict()
        self.properties['type']      = SquareType.Empty

    def getXY(self):
        y = int(self.id / 1000)
        x = self.id % 1000

        return [x, y]

    def setProperty(self, name, value):
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


class MapModel(QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self):
        QObject.__init__(self)

        self.width = 0
        self.height = 0
        self._squares = dict()

    def newMap(self, w, h):
        self.width = w
        self.height = h
        for row in range(h):
            for column in range(w):
                id = row*1000 + column
                self._squares[id] = MapSquareModel(id)

        self.updatedEntireMap.emit()

    def getSquare(self, id):
        return self._squares[id]


    def getSquareXY(self, row, column):
        id = row*1000 + column
        return self.getSquare(id)

    def getAllSquares(self):
        return self._squares

    def size(self):
        return [self.height, self.width]

    def toSerializableObj(self):
        squares = list()
        for id, square in self._squares.items():
            squares.append(square.toSerializableObj())

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
        for square in js['squares']:
            id = int(square['id'])
            obj = HouseMapSquareModel(id)
            obj.restoreFromJson(square)
            self._squares[id] = obj

    def saveMap(self, filename):
        extension = '.map'
        if not filename.endswith(extension):
            filename = filename + extension

        print("Saving map to " + filename)
        with open(filename, "w") as writeFile:
            json.dump(self.toSerializableObj(), writeFile, indent=4)

    def openMap(self, filename):
        extension = '.map'
        if not filename.endswith(extension):
            filename = filename + extension

        print("Loading map to " + filename)

        with open(filename, "r") as readFile:
            jsObj = json.load(readFile)
            self.restoreFromJson(jsObj)

        self.updatedEntireMap.emit()

