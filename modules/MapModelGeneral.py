from enum import Enum

import json


class MapModelGeneral():
    def __init__(self, squareModel):
        self._sqareModel = squareModel
        self.width = 0
        self.height = 0
        self._squares = dict()
        self._objects = list()
        self._updatedCallback = None

    def setUpdatedCallback(self, callback):
        self._updateCallback = callback

    def newMap(self, w, h):
        self.width = w
        self.height = h
        for row in range(h):
            for column in range(w):
                id = row*1000 + column
                self._squares[id] = self._sqareModel(id)

        if self._updateCallback is not None:
            self._updateCallback()

    def getSquare(self, id):
        return self._squares[id]


    def getSquareXY(self, row, column):
        id = row*1000 + column
        return self.getSquare(id)

    def getAllSquares(self):
        return self._squares

    def size(self):
        return [self.height, self.width]

    def addMapObject(self, obj):
        self._objects.append(obj)

    def toSerializableObj(self):
        squares = list()
        for id, square in self._squares.items():
            squares.append(square.toSerializableObj())

        objects = list()
        for obj in self._objects:
            objects.append(obj.toSerializableObj())

        obj = dict()
        obj['version'] = 1
        obj['squares'] = squares
        obj['objects'] = objects
        obj['width']   = self.width
        obj['height']  = self.height

        return obj

    def restoreFromJson(self, js):
        self.width  = js['width']
        self.height = js['height']

        self._squares = dict()
        for square in js['squares']:
            id = int(square['id'])
            obj = self._sqareModel(id)
            obj.restoreFromJson(square)
            self._squares[id] = obj

    def saveMap(self, filename):
        extension = '.json'
        if not filename.endswith(extension):
            filename = filename + extension

        print("Saving map to " + filename)
        with open(filename, "w") as writeFile:
            json.dump(self.toSerializableObj(), writeFile, indent=4)

    def openMap(self, filename):
        extension = '.json'
        if not filename.endswith(extension):
            filename = filename + extension

        print("Loading map to " + filename)

        with open(filename, "r") as readFile:
            jsObj = json.load(readFile)
            self.restoreFromJson(jsObj)

        if self._updateCallback is not None:
            self._updateCallback()

