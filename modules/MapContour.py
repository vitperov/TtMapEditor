from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

class MapContour(QObject):
    def __init__(self, model, canvas, tilesize, col, row, objCollection, redrawClbk):
        QObject.__init__(self)

        self._model = model
        self._canvas = canvas
        self._objCollection = objCollection
        self._tilesize = tilesize
        self._col = col
        self._row = row
        self._redrawClbk = redrawClbk

        self.updateState()

    def updateState(self):       
        sqType = self._model.getProperty('model')
        sqTypeDescription = self._objCollection.getObject(sqType)
        contourColor = sqTypeDescription.contour

        x = self._col * self._tilesize
        y = self._row * self._tilesize
        width = self._model.w * self._tilesize
        height = self._model.h * self._tilesize

        color = QtGui.QColor(contourColor)

        painter = QtGui.QPainter(self._canvas)
        painter.setPen(QtGui.QPen(color, 1))  # Set pen color and thickness

        # Draw the rectangle contour
        painter.drawRect(x, y, width, height)

        painter.end()
        self._redrawClbk()

