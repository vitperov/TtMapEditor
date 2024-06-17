from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

#from modules.HouseMapItem import *
from modules.MapItem import *
from modules.DeleteButtonItem import *

import math

class HouseMapPanel(QWidget):
    activeItemChanged = pyqtSignal(int, int)
    deleteRow         = pyqtSignal(int)
    deleteColumn      = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        self._model = None
        #self.squares = dict()
        self.items = []

        self._layout = QVBoxLayout()
        self._model = None

        self.setLayout(self._layout)
        
        self.label = QtWidgets.QLabel()
        self.label.mousePressEvent = self.onMouseClick
        canvas = QtGui.QPixmap(640, 480)
        canvas.fill(Qt.white)

        self._layout.addWidget(self.label)
        
    def onMouseClick(self, event):
        x = event.pos().x()
        y = event.pos().y() 
        print("Clicked X=" + str(x) + "; Y=" + str(y))
        col = int(x / self.pixPerTile)
        row = int(y / self.pixPerTile)
        print("Clicked row=" + str(row) + "; col=" + str(col))
        
        [rows, cols] = self._model.size()
        if row < rows and col < cols:
            self.activeItemChanged.emit(col, row)
        elif row == rows:
            print("Delete column idx=" + str(col))
            self.deleteColumn.emit(col)
        elif cols == cols:
            print("Delete row idx=" + str(row))
            self.deleteRow.emit(row)
        else:
            print("Error click outside canvas")

    def setModel(self, model):
        self._model = model

    def _createNewCanvas(self, editMode=False):
        [rows, cols] = self._model.size()
        
        if editMode:
            rows = rows + 1
            cols = cols + 1

        maxWidth = 1200;
        maxHeight = 800;

        wPixPerSquare = math.floor(maxWidth / cols)
        hPixPerSquare = math.floor(maxHeight / rows)
        self.pixPerTile = min(wPixPerSquare, hPixPerSquare)
        
        print("---> SIZE = " + str(cols*self.pixPerTile) + " x " +  str(rows*self.pixPerTile) + "; px= " + str(self.pixPerTile))
        
        canvas = QtGui.QPixmap(cols*self.pixPerTile, rows*self.pixPerTile)
        canvas.fill(Qt.blue)
        self.label.setPixmap(canvas)
        
    def redrawAll(self):
        [h, w] = self._model.size()
        
        print("=============== NEW CANVAS==============+")
        self._createNewCanvas(editMode=True)
        
        # TODO: delete previous items here
       
        self.items = []
        
        cv = self.label.pixmap()

        mapSquares = self._model.getAllSquares()
        for squareModel in mapSquares:
            item = MapItem(squareModel, cv, self.pixPerTile, squareModel.x, squareModel.y, self._model._objCollection)
            
            squareModel.changed.connect(item.updateState)
            self.items.append(item)
            
        # column delete buttons
        for x in range(w):
            item = DeleteButtonItem(cv, self.pixPerTile, x, h)
            # no need to store, will be garbage-collected
            
        # row delete buttons
        for y in range(h):
            item = DeleteButtonItem(cv, self.pixPerTile, w, y)
            # no need to store, will be garbage-collected


        #mapObjects = self._model.getAllObjects()
        #for mapObject in mapObjects:
        #    item = MapObjectItem(mapObject, cv, tilesize, mapObject.x, mapObject.y, self._model._objCollection)
        #    
        #    squareModel.changed.connect(item.updateState)
        #    items.append(item)
