from PyQt5.QtCore import *

import traceback
import json

from modules.GeometryPrimitives import *
from modules.commonModels.MapObjectModelGeneral import *
from modules.commonModels.SelectionRange import *

class AdditionalPropertyValue:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

class MapModelGeneral(QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self, squareModel, objCollection, texturesCollection):
        """
        squareModel is MapObjectModelGeneral
        objCollection is ?
        texturesCollection is TexturesCollection
        """
        QObject.__init__(self)
        self._sqareModel = squareModel
        self._objCollection = objCollection
        self._texturesCollection = texturesCollection
        self.width = 0
        self.height = 0
        self.editorWidth = 0
        self.editorHeight = 0;
        self._squares = list()
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

    def getSquare(self, x, y):
        #FIXME: depricated. Should use getSquareItems instead
        for square in self._squares:
            if square.x == x and square.y == y:
                return square

        return None

    def getSquareItems(self, x, y, z):
        items = list()
        for square in self._squares:
            if square.x == x and square.y == y and square.z == z:
                items.append(square)
        return items

    def getAreaSquareUniqueItems(self, selectionRange):
        items = list()
        seen_models = set()
        for square in self._squares:
            if selectionRange.startCol <= square.x <= selectionRange.endCol and selectionRange.startRow <= square.y <= selectionRange.endRow and square.z == selectionRange.zLevel:
                model = square.properties['model']
                if model not in seen_models:
                    seen_models.add(model)
                    items.append(square)
        return items

    def deleteSquareById(self, id):
        print("Deleting entire square, id=" + str(id))
        N = len(self._squares);
        for i in range(N):
            if self._squares[i].id == id:
                del self._squares[i]
                if self._updateCallback is not None:
                    self._updateCallback()
                return

    #FIXME: These 3 functions do almost the same
    def createEmpySquareAt(self, row, column):
        obj = self._sqareModel()
        obj.y = row
        obj.x = column
        self._squares.append(obj)

    def createObjectAt(self, x, y, z):
        obj = self._sqareModel()
        obj.x = x
        obj.y = y
        obj.z = z
        self._squares.append(obj)
        return obj

    def addMapObject(self, obj):
        self._squares.append(obj)
    
    # ---------------

    def createObjectsInSelection(self, selectionRange):
        """Creates a new object in each square within the specified selection range."""
        for row in range(selectionRange.startRow, selectionRange.endRow + 1):
            for col in range(selectionRange.startCol, selectionRange.endCol + 1):
                self.createObjectAt(col, row, selectionRange.zLevel)

    def deleteObjectsInSelection(self, selectionRange, model=None):
        """Deletes all objects within the specified selection range. If model is provided, only delete objects with the matching model."""
        i = 0
        while i < len(self._squares):
            square = self._squares[i]
            if (selectionRange.startCol <= square.x <= selectionRange.endCol and 
                selectionRange.startRow <= square.y <= selectionRange.endRow and 
                square.z == selectionRange.zLevel and
                (model is None or square.properties['model'] == model)):
                del self._squares[i]
            else:
                i += 1

        if self._updateCallback:
            self._updateCallback()

    def deleteRow(self, rowId): # _squares nice here, but what about _objects?
        # delete row
        self._squares[:] = filter(lambda item: item.y != rowId, self._squares)

        # shift coordinates
        for square in self._squares:
            if square.y > rowId:
                square.y = square.y - 1

        # add empy row at the end
        for column in range(self.width):
            self.createEmpySquareAt(self.height - 1, column)
            
        self.height -= 1

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
            
        self.width -= 1

        self._updateCallback()

    def addRow(self, before=None):
        """Adds a new row at the specified position or at the bottom of the map."""
        if before is None:
            for column in range(self.width):
                self.createEmpySquareAt(self.height, column)  # New row at the end
            self.height += 1  # Increase the height count
        else:
            for square in self._squares:
                if square.y >= before:
                    square.y += 1
            for column in range(self.width):
                self.createEmpySquareAt(before, column)  # New row at the specified position
            self.height += 1

        if self._updateCallback:
            self._updateCallback()

    def addColumn(self, before=None):
        """Adds a new column at the specified position or to the right side of the map."""
        if before is None:
            for row in range(self.height):
                self.createEmpySquareAt(row, self.width)  # New column on the right
            self.width += 1  # Increase the width count
        else:
            for square in self._squares:
                if square.x >= before:
                    square.x += 1
            for row in range(self.height):
                self.createEmpySquareAt(row, before)  # New column at the specified position
            self.width += 1

        if self._updateCallback:
            self._updateCallback()
            
    def getAllSquares(self, zLevel):
        items = list()
        for square in self._squares:
            if square.z == zLevel:
                items.append(square)
        return items
        
    def getAllObjectOfType(self, modelType, selectionRange=None):
        result = []
        for obj in self._squares:
            isInSelectionRange = (selectionRange is None or
                                  (selectionRange.startCol <= obj.x <= selectionRange.endCol and
                                   selectionRange.startRow <= obj.y <= selectionRange.endRow and
                                   obj.z == selectionRange.zLevel))
            if isInSelectionRange and (modelType is None or obj.properties.get('model') == modelType):
                result.append(obj)
        return result

    def size(self):
        return [self.height, self.width]

    def toSerializableObj(self):
        squares = list()
        for square in self._squares:
            squares.append(square.toSerializableObj())

        obj = dict()
        obj['version'] = 1
        obj['squares'] = squares
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
            filename = extension + filename

        print("Loading map from " + filename)

        with open(filename, "r") as readFile:
            jsObj = json.load(readFile)
            self.restoreFromJson(jsObj)

        if self._updateCallback is not None:
            self._updateCallback()
            
    def updateEntireMap(self):
        self.updatedEntireMap.emit()
        
    def setGroupProperty(self, selectionRange, modelFilter, property, value):
        for square in self._squares:
            if selectionRange.startCol <= square.x <= selectionRange.endCol and selectionRange.startRow <= square.y <= selectionRange.endRow and square.z == selectionRange.zLevel:
                if square.properties['model'] == modelFilter:
                    square.setProperty(property, value)
                    self.updateModelSize(square)

    def updateModelSize(self, square):
        model_name = square.getProperty('model')
        map_object = self._objCollection.getObject(model_name)
        if map_object:
            square.w = map_object.w
            square.h = map_object.h

    def overwriteEverythingWith(self, selectionRange, modelType):
        """Deletes all objects within the specified selection range and fills it with new objects of the given model type."""
        self.deleteObjectsInSelection(selectionRange)
        for row in range(selectionRange.startRow, selectionRange.endRow + 1):
            for col in range(selectionRange.startCol, selectionRange.endCol + 1):
                new_square = self.createObjectAt(col, row, selectionRange.zLevel)
                new_square.setModel(modelType)

        if self._updateCallback:
            self._updateCallback()
