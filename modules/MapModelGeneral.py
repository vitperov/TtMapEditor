from enum import Enum

import json

class MapObjectModelGeneral:
    def __init__(self, x, y):
        self.classnames = dict()

        self.properties = dict()

        self.x = x
        self.y = y

    def toSerializableObj(self):
        # properties are enums, they can't be directly converted to int
        obj = dict()
        for name, prop in self.properties.items():
            value = prop
            obj[name] = value

        obj['x'] =  self.x
        obj['y'] =  self.y

        return obj
        
    def getProperty(self, name):
        return self.properties[name]
        
    def restoreFromJson(self, js):
        self.x = js['x']
        self.y = js['y']
        
        for propName, propClass in self.classnames.items():
            self.properties[propName] = propClass(js[propName])

class MapModelGeneral():
    def __init__(self, squareModel):
        self._sqareModel = squareModel
        self.width = 0
        self.height = 0
        self._squares = list()
        self._objects = list()
        self._updatedCallback = None

    def setUpdatedCallback(self, callback):
        self._updateCallback = callback

    def newMap(self, w, h):
        self.width = w
        self.height = h
        for row in range(h):
            for column in range(w):
                obj = self._sqareModel()
                obj.y = row
                obj.x = column
                self._squares.append(obj)

        if self._updateCallback is not None:
            self._updateCallback()

    def getSquare(self, x, y):
        #FIXME: depricated. Should use getSquareItems instead
        for square in self._squares:
            if square.x == x and square.y == y:
                return square

        return None
        
    def getSquareItems(self, x, y):
        # FIXME: Multiple square items are not supported yet
        items = list()
        items.append(self.getSquare(x, y))
        return items

    def getAllSquares(self):
        return self._squares

    def size(self):
        return [self.height, self.width]

    def addMapObject(self, obj):
        self._objects.append(obj)

    def toSerializableObj(self):
        squares = list()
        for square in self._squares:
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

        self._squares = list()
        for square in js['squares']:
            obj = self._sqareModel()
            obj.restoreFromJson(square)
            self._squares.append(obj)

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

