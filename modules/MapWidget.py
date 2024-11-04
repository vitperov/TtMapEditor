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
    multipleSelection = pyqtSignal(int, int, int, int, int)

    def __init__(self):
        QWidget.__init__(self)
        self._model = None
        self.zLevel = 0
        #self.isMultipleSelect = False

        self._layout = QVBoxLayout()
        self._model = None

        self.setLayout(self._layout)

        self.label = QtWidgets.QLabel()
        self.label.mousePressEvent = self.onMousePress
        self.label.mouseReleaseEvent = self.onMouseRelease

        self._canvas = QtGui.QPixmap(640, 480)
        self._canvas.fill(Qt.white)

        self._layout.addWidget(self.label)
        self._layout.addStretch()

        self.selectedRow = None
        self.selectedCol = None
        self.startPoint = None
        self.endPoint = None

        self.updateCanvas()

    def updateCanvas(self):
        self.label.setPixmap(self._canvas)

    def onMousePress(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.startPoint = (x, y)

    def onMouseRelease(self, event):
        if not self.startPoint:
            return

        x1, y1 = self.startPoint
        x2 = event.pos().x()
        y2 = event.pos().y()

        print(f"Mouse press point: ({x1}, {y1})")
        print(f"Mouse release point: ({x2}, {y2})")

        startCol = int(min(x1, x2) / self.pixPerTile)
        endCol = int(max(x1, x2) / self.pixPerTile)
        startRow = int(min(y1, y2) / self.pixPerTile)
        endRow = int(max(y1, y2) / self.pixPerTile)

        print(f"Selected area converted to cell coordinates: Start({startCol}, {startRow}), End({endCol}, {endRow})")

        [rows, cols] = self._model.size()

        self.endPoint = (endCol, endRow)

       
        
        if startRow < rows and startCol < cols:
            self.selectedRow = startRow
            self.selectedCol = startCol
            self.multipleSelection.emit(startCol, startRow, endCol, endRow, self.zLevel)
            if (startCol == endCol) and (startRow == endRow):
                self.activeItemChanged.emit(startCol, startRow, self.zLevel)
                
        elif startRow == rows and startCol == cols:
            print("Clicked corner. No actions")
        elif startRow == rows:
            print("Delete column idx=" + str(startCol))
            self.deleteColumn.emit(startCol)
        elif startCol == cols:
            print("Delete row idx=" + str(startRow))
            self.deleteRow.emit(startRow)

        self.redrawAll()
        self.startPoint = None
        self.endPoint = None

    def setModel(self, model):
        self._model = model

    def _createNewCanvas(self, editMode=False):
        [rows, cols] = self._model.size()

        if editMode:
            rows = rows + 1
            cols = cols + 1

        maxWidth = 1400
        maxHeight = 900

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

        if self.selectedRow is not None and self.selectedCol is not None:
            # Draw a red rectangle around the selected square
            selectionPen = QtGui.QPen(QtGui.QColor('#FF0000'))  # red color
            selectionPen.setStyle(QtCore.Qt.SolidLine)
            selectionPen.setWidth(2)
            painter.setPen(selectionPen)

            if self.endPoint:
                startCol, startRow = self.selectedCol, self.selectedRow
                endCol, endRow = self.endPoint
                x = startCol * self.pixPerTile
                y = startRow * self.pixPerTile
                w = (endCol - startCol + 1) * self.pixPerTile
                h = (endRow - startRow + 1) * self.pixPerTile
                painter.drawRect(x, y, w, h)
            else:
                painter.drawRect(self.selectedCol * self.pixPerTile, self.selectedRow * self.pixPerTile, self.pixPerTile, self.pixPerTile)

        painter.end()
        self.updateCanvas()

    def redrawAll(self):
        [h, w] = self._model.size()
        print("=============== NEW CANVAS==============+")
        self._createNewCanvas(editMode=True)
        mapSquares = self._model.getAllSquares(self.zLevel)
        #mapObjects = self._model.getAllObjects()
        #mapAll = (mapSquares + mapObjects)
        #print('len of mapAll: ', len(mapAll))
        for squareModel in mapSquares:
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

    #def onMultipleSelectionChanged(self, isMultiple):
    #    self.isMultipleSelect = isMultiple
    #    print(f"Multiple selection changed: {isMultiple}")
