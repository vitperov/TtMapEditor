from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

import os.path

# FIXME: it's copypaste of MapItem. Refactoring needed
class MapObjectItem(QObject):
    def __init__(self, model, canvas, tilesize, col, row, objCollection):
        QObject.__init__(self)

        self._model = model
        self._objCollection = objCollection
        self._canvas = canvas
        self._tilesize = tilesize
        self._col = col
        self._row = row

        size = QSize(self._tilesize, self._tilesize)

        self.updateState()


    def updateState(self):
        sqType      = self._model.getProperty('model')

        #imgFile = "resources/MapSquare/" + sqTypeName + ".png"
        imgFile = self._objCollection.getIcon(sqType)
        if not os.path.isfile(imgFile):
            print("type " + sqTypeName + " not found")
            return

        pixmap = QtGui.QPixmap(imgFile)
        size = QSize(self._tilesize, self._tilesize)

        scaledPixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
       
        x = self._col * self._tilesize
        y = self._row * self._tilesize
        
        painter = QtGui.QPainter(self._canvas)
        painter.drawPixmap(x, y, scaledPixmap)
        
        painter.end()

