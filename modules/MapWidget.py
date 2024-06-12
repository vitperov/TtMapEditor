from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

import math

from modules.MapItem import *
from modules.MapObjectItem import *

class MapWidget(QWidget):
    activeItemChanged = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        self._layout = QVBoxLayout()
        self._model = None

        self.setLayout(self._layout)
        
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(640, 480)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        self._layout.addWidget(self.label)

    def onItemClicked(self, itemId):
        print("Item clicked Id=" + str(itemId))
        self.activeItemChanged.emit(itemId)


    def setModel(self, model):
        self._model = model
        
    def _createNewCanvas(self):
        [rows, cols] = self._model.size()

        maxWidth = 1200;
        maxHeight = 1000;
        
        wPixPerSquare = math.floor(maxWidth / cols)
        hPixPerSquare = math.floor(maxHeight / rows)
        pixPerSquare = min(wPixPerSquare, hPixPerSquare)
        
        print("---> SIZE = " + str(cols*pixPerSquare) + " x " +  str(rows*pixPerSquare) + "; px= " + str(pixPerSquare))
        
        canvas = QtGui.QPixmap(cols*pixPerSquare, rows*pixPerSquare)
        canvas.fill(Qt.blue)
        self.label.setPixmap(canvas)

        return pixPerSquare
        
    def redrawAll(self):
        [h, w] = self._model.size()
        
        print("=============== NEW CANVAS==============+")
        tilesize = self._createNewCanvas()
        
        # TODO: delete previous items here
       
        items = []
        
        cv = self.label.pixmap()

        mapSquares = self._model.getAllSquares()
        for squareModel in mapSquares:
            item = MapItem(squareModel, cv, tilesize, squareModel.x, squareModel.y, self._model._objCollection)
            
            squareModel.changed.connect(item.updateState)
            items.append(item)

        mapObjects = self._model.getAllObjects()
        for mapObject in mapObjects:
            item = MapObjectItem(mapObject, cv, tilesize, mapObject.x, mapObject.y, self._model._objCollection)
            
            squareModel.changed.connect(item.updateState)
            items.append(item)
