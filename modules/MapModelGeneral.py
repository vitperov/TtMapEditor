from enum import Enum
from PyQt5.QtCore import *

import json
import uuid

class ObjectRotation(str, Enum):
    deg0    = '0'
    deg90   = '90'
    deg180  = '180'
    deg270  = '270'

class MapObjectModelGeneral(QObject):
    changed = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.classnames = dict()
        self.properties = dict()

        self.classnames['rotation']  = ObjectRotation
        self.properties['rotation']  = ObjectRotation.deg0

        self.classnames['model']      = str
        self.properties['model']      = "Empty"

        self.classnames['variant']      = str
        self.properties['variant']      = ""

        self.id = str(uuid.uuid4())

        self.x = 0
        self.y = 0
        self.w = 1
        self.h = 1

    def init(self, x, y, model, rotation=ObjectRotation.deg0, w=1, h=1, variant=""):
        self.x = x
        self.y = y
        self.properties['model']    = model
        self.properties['rotation'] = rotation
        self.properties['variant'] = variant
        self.w = w
        self.h = h

    def toSerializableObj(self):
        # properties are enums, they can't be directly converted to int
        obj = dict()
        for name, prop in self.properties.items():
            value = prop
            obj[name] = value

        obj['x'] =  self.x
        obj['y'] =  self.y
        obj['w'] =  self.w
        obj['h'] =  self.h
        obj['id'] = self.id

        return obj

    def getProperty(self, name):
        return self.properties[name]

    def setProperty(self, name, value):
        variableClass = self.classnames[name]
        self.properties[name] = variableClass(value)
        self.changed.emit()

    def restoreFromJson(self, js):
        self.x = js['x']
        self.y = js['y']
        self.w = js.get('w', 1)
        self.h = js.get('h', 1)

        if ('id' in js) and (len(js['id'])) > 0:
            self.id = js['id']
        else:
            self.id = str(uuid.uuid4())

        for propName, propClass in self.classnames.items():
            self.properties[propName] = propClass(js[propName])

class MapModelGeneral(QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self, squareModel, objCollection):
        QObject.__init__(self)
        self._sqareModel = squareModel
        self._objCollection = objCollection
        self.width = 0
        self.height = 0
        self.editorWidth = 0
        self.editorHeight = 0;
        self._squares = list()
        self._objects = list()
        self._updateCallback = self.updateEntireMap

    def setUpdatedCallback(self, callback):
        self._updateCallback = callback

    def newMap(self, w, h):
        self.width = w
        self.height = h
        for row in range(h):
            for column in range(w):
                self.createEmpySquareAt(row, column)

        if self._updateCallback is not None:
            self._updateCallback()

    def createEmpySquareAt(self, row, column):
        obj = self._sqareModel()
        obj.y = row
        obj.x = column
        self._squares.append(obj)

    def getSquare(self, x, y):
        #FIXME: depricated. Should use getSquareItems instead
        for square in self._squares:
            if square.x == x and square.y == y:
                return square

        return None

    def getSquareItems(self, x, y):
        items = list()
        for square in self._squares:
            if square.x == x and square.y == y:
                items.append(square)
        return items

    # TODO: used only for house square and deletes object, not sqare
    # We should rename it, or better refactor everything and use only objects
    def deleteSquareById(self, id):
        print("Deleting entire square, id=" + str(id))
        N = len(self._squares);
        for i in range(N):
            if self._squares[i].id == id:
                del self._squares[i]
                if self._updateCallback is not None:
                    self._updateCallback()
                return

    def createObjectAt(self, x, y):
        obj = self._sqareModel()
        obj.x = x
        obj.y = y
        self._squares.append(obj)
        return obj

    def deleteRow(self, rowId):
        # delete row
        self._squares[:] = filter(lambda item: item.y != rowId, self._squares)

        # shift coordinates
        for square in self._squares:
            if square.y > rowId:
                square.y = square.y - 1

        # add empy row at the end
        for column in range(self.width):
            self.createEmpySquareAt(self.height - 1, column)

        self._updateCallback()

    def deleteColumn(self, columnId):
        #delete column
        self._squares[:] = filter(lambda item: item.x != columnId, self._squares)

        # shift coordinates
        for square in self._squares:
            if square.x > columnId:
                square.x = square.x - 1

        # add empy column at the end
        for row in range(self.height):
            self.createEmpySquareAt(row, self.width - 1)

        self._updateCallback()


    def getAllSquares(self):
        return self._squares
        
    def getAllObjects(self):
        return self._objects
        
    # iterates (squares + objects)
    def getAllObjectOfType(self, modelType):
        result = []
        for obj in self._objects + self._squares:
            if obj.properties.get('model') == modelType:
                result.append(obj)
        return result

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
        self.width  = max(js['width'], self.editorWidth)
        self.height = max(js['height'], self.editorHeight)

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

        print("Loading map from " + filename)

        with open(filename, "r") as readFile:
            jsObj = json.load(readFile)
            self.restoreFromJson(jsObj)

        if self._updateCallback is not None:
            self._updateCallback()
            
    def updateEntireMap(self):
        self.updatedEntireMap.emit()

