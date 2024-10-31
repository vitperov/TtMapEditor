from enum import Enum

from PyQt5.QtCore import *

import traceback
import json
import uuid # we use it as string
from numbers import Number # not only integer

def isclass (obj):
    """Return true if the obj is a class.
    Class objects provide these attributes:
        __doc__         documentation string
        __module__      name of module in which this class was defined"""
    try:
        import types
        return isinstance(obj, (type, types.ClassType,))
    except:
        return isinstance(obj, (type,))

class ObjectRotation(str, Enum):
    deg0    = '0'
    deg90   = '90'
    deg180  = '180'
    deg270  = '270'

class MapObjectModelGeneral(QObject):
    changed = pyqtSignal()

    def __init__(self, id=None): # TODO FIX: why second init??
        QObject.__init__(self)
        self.classnames = dict()
        self.properties = dict()
        
        self.model = "Empty"
        self.modelSuper = None

        self.classnames['rotation']  = ObjectRotation
        self.properties['rotation']  = ObjectRotation.deg0

        self.classnames['model']      = str
        self.properties['model']      = "Empty"

        self.classnames['variant']      = str
        self.properties['variant']      = ""

        self.id = str(id) if (id is not None) else str(uuid.uuid4())

        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 1
        self.h = 1

    def init(self, x, y, model, rotation=ObjectRotation.deg0, w=1, h=1, variant="", id=None, modelSuper=None):
        self.id = str(id) if (id is not None) else str(uuid.uuid4()) # FIXED: id was missing
        self.x = x
        self.y = y
        self.z = 0
        self.modelSuper = None if (modelSuper is None or not(modelSuper)) else modelSuper # It is just model super replacer on comparation e.g. for LandLotContent
        #self.modelGenerator = modelGenerator # model generator type
        self.model = model # model generator type
        self.properties['model']    = model # model name (where it is used?)
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
        obj['z'] =  self.z
        obj['w'] =  self.w
        obj['h'] =  self.h
        obj['id'] = self.id
        obj['model'] = self.properties['model']

        return obj
        
    def __hash__(self):
        return hash(self.toSerializableObj())
        
    def __eq__(self, other):
        try:
            if isinstance(other, self.__class__):
                #print('self', self.__dict__)
                #print('other', other.__dict__)
                if (self.id == other.id):
                    return True
                tmp_self = dict(self.__dict__)
                tmp_other = dict(other.__dict__)
                del tmp_self['id']
                del tmp_other['id']
                return tmp_self == tmp_other
        except Exception as e1:
            print(traceback.format_exc())
            #raise e1
        return None #return NotImplemented
            
    def __lt__(self, other):
        if ((self.x) == (other.x) and (self.y) == (other.y)):
            return self.id < other.id
        return ((self.x) < (other.x) or (self.y) < (other.y))
        
    def __gt__(self, other):
        if ((self.x) == (other.x) and (self.y) == (other.y)):
            return self.id > other.id
        return ((self.x) > (other.x) or (self.y) > (other.y))

    def getProperty(self, name):
        return self.properties[name]

    def setProperty(self, name, value):
        variableClass = self.classnames[name]
        self.properties[name] = variableClass(value)
        self.changed.emit()

    def restoreFromJson(self, js):
        self.x = js['x']
        self.y = js['y']
        self.z = js.get('z', 0)
        self.w = js.get('w', 1)
        self.h = js.get('h', 1)

        if ('id' in js) and (len(js['id'])) > 0:
            self.id = js['id']
        else:
            self.id = str(uuid.uuid4())

        for propName, propClass in self.classnames.items():
            self.properties[propName] = propClass(js.get(propName,""))

class MapModelGeneral(QObject):
    updatedEntireMap = pyqtSignal()
    def __init__(self, squareModel, objCollection):
        """
        squareModel is MapObjectModelGeneral
        objCollection is ?
        """
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

    def getSquareItems(self, x, y, z):
        items = list()
        for square in self._squares:
            if square.x == x and square.y == y and square.z == z:
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

    def createObjectAt(self, x, y, z):
        obj = self._sqareModel()
        obj.x = x
        obj.y = y
        obj.z = z
        self._squares.append(obj)
        return obj

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

    def addRow(self):
        """Adds a new row at the bottom of the map."""
        for column in range(self.width):
            self.createEmpySquareAt(self.height, column)  # New row at the end

        self.height += 1  # Increase the height count
        if self._updateCallback:
            self._updateCallback()

    def addColumn(self):
        """Adds a new column to the right side of the map."""
        for row in range(self.height):
            self.createEmpySquareAt(row, self.width)  # New column on the right

        self.width += 1  # Increase the width count
        if self._updateCallback:
            self._updateCallback()
            
    #def recalculateMapSize(self):
    #    maxX = 0
    #    maxY = 0
    #    for square in self._squares:
    #        maxX = max(maxX, square.x)
    #        maxY = max(maxY, square.y)
    #        
    #    self.width = maxX + 1
    #    self.height = maxY + 1

    def getAllSquares(self, zLevel):
        items = list()
        for square in self._squares:
            if square.z == zLevel:
                items.append(square)
        return items
        
    def getAllObjects(self):
        return self._objects
        
    # iterates (squares + objects)
    def getAllObjectOfType(self, modelType):
        result = []
        for obj in self._objects + self._squares:
            if (obj.properties.get('model') == modelType or obj.modelSuper == modelType):
                result.append(obj)
        return result

    def size(self):
        return [self.height, self.width]

    def addMapObject(self, obj):
        self._objects.append(obj)
        
    def removeMapObject(self, objOrId, modelOrType = '*'):
        '''
        Remove the map object:
        objOrId - the object or the string id of object
        modelOrType - filter by model generator class or model generator class name
        '''
        tmp = None
        actualModel = None
        try:
            if (isinstance(objOrId, Number)):
                objOrId = str(objOrId)
            if (isinstance(objOrId, str)):
                tmp = MapObjectModelGeneral(id = objOrId)
                if (tmp in self._objects):
                    tmp = self._objects[self._objects.index(tmp)]
                elif (tmp in self._squares):
                    tmp = self._squares[self._squares.index(tmp)]
                else:
                    return False
            else:
                tmp = objOrId
            try:
                if (tmp.modelSuper is not None):
                    print('tmp.model: ', tmp.model, tmp.modelSuper)
            except:
                pass
            actualModel = tmp.model;  tmp.model = tmp.modelSuper if (tmp.modelSuper is not None) else tmp.model # It is because of strange LandLotContent
            #print('tmp0: ', tmp)
            #print('modelOrType: ', modelOrType)
            if (isinstance(modelOrType, str)):
                #print('str', modelOrType, tmp.model)
                #print('*' != modelOrType)
                #print(tmp.model != modelOrType)
                #print(tmp.__class__.__name__ != modelOrType)
                #print((isclass(tmp.model) and tmp.model.__name__ != modelOrType))
                if ('*' != modelOrType and tmp.model != modelOrType and tmp.__class__.__name__ != modelOrType and (not isclass(tmp.model) or (isclass(tmp.model) and tmp.model.__name__ != modelOrType))):
                    #print('str bad')
                    return None
                #print('str good')
            elif (not isinstance(tmp, modelOrType) and tmp.model != modelOrType):
                #print('type bad: ', tmp, modelOrType)
                return None
            #print('good')
            if (tmp in self._objects):
                self._objects.remove(tmp)
            else:
                self._squares.remove(tmp)
            return True
        finally:
            if (actualModel is not None and (tmp is not None) and isinstance(tmp, MapObjectModelGeneral)):
                tmp.model = actualModel
        
    def removeAllMapObjects(self, modelOrType):
        was = None
        try:
            if ('*' == modelOrType):
                print('* is not allowed here')
                return was
            was = False
            tmps = list(self._objects) + list(self._squares)
            for obj in tmps:
                if (self.removeMapObject(obj, modelOrType)): ##### if (self.removeMapObject(obj.id, modelOrType)):
                    was = True
        except:
            #print(e1)
            print(traceback.format_exc())
        finally:
            return was

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

        self._objects = list()
        for jsObj in js['objects']:
            obj = self._sqareModel()
            obj.restoreFromJson(jsObj)
            self._objects.append(obj)

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
