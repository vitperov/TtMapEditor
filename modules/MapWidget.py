from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.MapItemDrawer import *
from modules.DeleteButtonItem import *

import math

class MapWidget(QWidget):
    activeItemChanged = pyqtSignal(int, int, int)
    deleteRow         = pyqtSignal(int)
    deleteColumn      = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        self._model = None
        self.zLevel = 0;

        self._layout = QVBoxLayout()
        self._model = None

        self.setLayout(self._layout)

        self.label = QtWidgets.QLabel()
        self.label.mousePressEvent = self.onMouseClick

        self._canvas = QtGui.QPixmap(640, 480)
        self._canvas.fill(Qt.white)

        self._layout.addWidget(self.label)
        self._layout.addStretch()

        self.updateCanvas()

    def updateCanvas(self):
        self.label.setPixmap(self._canvas)

    def onMouseClick(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print("Clicked X=" + str(x) + "; Y=" + str(y))
        col = int(x / self.pixPerTile)
        row = int(y / self.pixPerTile)
        print("Clicked row=" + str(row) + "; col=" + str(col))

        [rows, cols] = self._model.size()
        if row < rows and col < cols:
            self.activeItemChanged.emit(col, row, self.zLevel)
        elif row == rows and col == cols:
            print("Clicked corner. No actions")
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

        maxWidth = 1400;
        maxHeight = 900;

        wPixPerSquare = math.floor(maxWidth / cols)
        hPixPerSquare = math.floor(maxHeight / rows)
        self.pixPerTile = min(wPixPerSquare, hPixPerSquare)

        print("---> SIZE = " + str(cols*self.pixPerTile) + " x " +  str(rows*self.pixPerTile) + "; px= " + str(self.pixPerTile))

        self._canvas = QtGui.QPixmap(cols*self.pixPerTile, rows*self.pixPerTile)
        self._canvas.fill(QtGui.QColor('#ADD8E6')) # light blue

        # Draw dashed lines between squares
        painter = QtGui.QPainter(self._canvas)
        pen = QtGui.QPen(QtGui.QColor('#000000'))  # black color
        pen.setStyle(QtCore.Qt.DashLine)
        pen.setWidth(1)
        painter.setPen(pen)

        for x in range(0, cols*self.pixPerTile, self.pixPerTile):
            painter.drawLine(x, 0, x, rows*self.pixPerTile)
        for y in range(0, rows*self.pixPerTile, self.pixPerTile):
            painter.drawLine(0, y, cols*self.pixPerTile, y)

        painter.end()
        self.updateCanvas()

    def redrawAll(self):
        [h, w] = self._model.size()
        print("=============== NEW CANVAS==============+")
        self._createNewCanvas(editMode=True)
        mapSquares = self._model.getAllSquares(self.zLevel)
        mapObjects = self._model.getAllObjects()
        mapAll = (mapSquares + mapObjects)
        print('len of mapAll: ', len(mapAll))
        for squareModel in mapAll:
            # Don not store. It's one-time object that just draws an object
            item = MapItemDrawer(squareModel, self._canvas, self.pixPerTile, self._model._objCollection, self.updateCanvas)

        # column delete buttons
        for x in range(w):
            item = DeleteButtonItem(self._canvas, self.pixPerTile, x, h)
            # no need to store, will be garbage-collected

        # row delete buttons
        for y in range(h):
            item = DeleteButtonItem(self._canvas, self.pixPerTile, w, y)
            # no need to store, will be garbage-collected


        self.updateCanvas()
