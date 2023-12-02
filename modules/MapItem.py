from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

class MapItem(QObject):
    clicked = pyqtSignal(int, int)

    def __init__(self, model, canvas, tilesize, col, row):
        QObject.__init__(self)

        self._model = model
        self._canvas = canvas
        self._tilesize = tilesize
        self._col = col
        self._row = row

        size = QSize(self._tilesize, self._tilesize)

        #self.widget = QtGui.QLabel(self)

        #self._layout = QVBoxLayout()
        #self._layout.addWidget(self.widget)
        #self._layout.setContentsMargins(0,0,0,0)

        #self.setLayout(self._layout)

        self.updateState()


    def updateState(self):
        #self.widget.setParent(None)
        #self.widget = QtGui.QLabel(self)

        sqType      = self._model.getProperty('type')
        sqTypeName = sqType

        imgFile = "resources/MapSquare/" + sqTypeName + ".png"
        pixmap = QtGui.QPixmap(imgFile)
        #transform = QtGui.QTransform().rotate(rotIdToAngle(rotation))
        size = QSize(self._tilesize, self._tilesize)

        scaledPixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        #self.widget.setPixmap(scaledPixmap)
        #self.widget.setFixedSize(size)

        #self.widget.setStyleSheet("background-color: lightgray")
        #self._layout.addWidget(self.widget)
        
        x = self._col * self._tilesize
        y = self._row * self._tilesize
        
        painter = QtGui.QPainter(self._canvas)
        painter.drawPixmap(x, y, scaledPixmap)
        
        painter.end()
        #self.update()


    def mousePressEvent(self, event):
        self.clicked.emit(self._model.x, self._model.y)

