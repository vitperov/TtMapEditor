from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

class MapItem(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, model):
        QWidget.__init__(self)

        self._model = model
        self.id = self._model.id
        self._tilesize = 16

        size = QSize(self._tilesize, self._tilesize)

        self.widget = QtGui.QLabel(self)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self.widget)
        self._layout.setContentsMargins(0,0,0,0)

        self.setLayout(self._layout)

        self.updateState()


    def updateState(self):
        self.widget.setParent(None)
        self.widget = QtGui.QLabel(self)

        sqType      = self._model.getProperty('type')
        sqTypeName = sqType

        imgFile = "resources/MapSquare/" + sqTypeName + ".png"
        pixmap = QtGui.QPixmap(imgFile)
        #transform = QtGui.QTransform().rotate(rotIdToAngle(rotation))
        size = QSize(self._tilesize, self._tilesize)

        scaledPixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        self.widget.setPixmap(scaledPixmap)
        self.widget.setFixedSize(size)

        self.widget.setStyleSheet("background-color: lightgray")
        self._layout.addWidget(self.widget)


    def mousePressEvent(self, event):
        self.clicked.emit(self.id)

