from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

class MapItemDrawer(QObject):
    def __init__(self, model, canvas, tilesize, objCollection, redrawClbk):
        QObject.__init__(self)

        self._model = model
        self._objCollection = objCollection
        self._canvas = canvas
        self._tilesize = tilesize
        self._col = model.x
        self._row = model.y
        self._redrawClbk = redrawClbk;

        size = QSize(self._tilesize, self._tilesize)

        self.updateState()


    def updateState(self):
        sqType      = self._model.getProperty('model')
        rotation    = self._model.getProperty('rotation')

        imgFile = self._objCollection.getIcon(sqType)
        pixmap = QtGui.QPixmap(imgFile)

        transform = QtGui.QTransform().rotate(int(rotation))
        rotatedPixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)

        size = QSize(self._tilesize, self._tilesize)
        scaledPixmap = rotatedPixmap.scaled(size, QtCore.Qt.KeepAspectRatio)

        x = self._col * self._tilesize
        y = self._row * self._tilesize
        
        painter = QtGui.QPainter(self._canvas)
        painter.drawPixmap(x, y, scaledPixmap)
        
        painter.end()
        self._redrawClbk()

