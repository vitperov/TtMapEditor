from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

class MapItemDrawer:
    def __init__(self, model, canvas, tilesize, objCollection, redrawClbk):

        self._model = model
        self._objCollection = objCollection
        self._canvas = canvas
        self._tilesize = tilesize
        self._col = model.x
        self._row = model.y
        self._redrawClbk = redrawClbk;

        size = QSize(self._tilesize, self._tilesize)
        
        self.sqType = self._model.getProperty('model')
        isContour = objCollection.isContour(self.sqType)
        #print(f"{self.sqType} -> {isContour}")

        if isContour:
            self.drawContour()
        else:
            self.drawPixmap()

    def drawPixmap(self):
        rotation    = self._model.getProperty('rotation')

        imgFile = self._objCollection.getIcon(self.sqType)
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
        
    def drawContour(self):
        sqTypeDescription = self._objCollection.getObject(self.sqType)
        contourColor = sqTypeDescription.contour

        x = self._col * self._tilesize
        y = self._row * self._tilesize
        width = self._model.w * self._tilesize
        height = self._model.h * self._tilesize

        color = QtGui.QColor(contourColor)

        painter = QtGui.QPainter(self._canvas)
        painter.setPen(QtGui.QPen(color, 1))  # Set pen color and thickness

        # Draw the rectangle contour
        #print(f"{sqType} -> {contourColor} -> {x} {y} {width} {height}")
        painter.drawRect(x, y, width, height)

        painter.end()
        self._redrawClbk()

