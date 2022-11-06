from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

from modules.Model import *

def rotIdToAngle(rotStr):
    return int(rotStr);

class HouseMapItem(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, model):
        QWidget.__init__(self)

        self._model = model
        self.id = self._model.id
        self._tilesize = 64

        size = QSize(self._tilesize, self._tilesize)

        self.widget = QtGui.QLabel(self)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self.widget)
        self._layout.setContentsMargins(0,0,0,0)

        self.setLayout(self._layout)

        self.updateState()


    def updateState(self):
        sqType      = self._model.getProperty('type')
        rotation    = self._model.getProperty('rotation')
        territory   = self._model.getProperty('territory')

        self.widget.setParent(None)
        self.widget = QtGui.QLabel(self)

        sqTypeName = sqType
        imgFile = "resources/SquareType/" + sqTypeName + ".png"
        pixmap = QtGui.QPixmap(imgFile)
        transform = QtGui.QTransform().rotate(rotIdToAngle(rotation))
        size = QSize(self._tilesize, self._tilesize)
        rotatedPixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)

        scaledPixmap = rotatedPixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        self.widget.setPixmap(scaledPixmap)
        self.widget.setFixedSize(size)

        self.widget.setStyleSheet("background-color: lightgray")
        self._layout.addWidget(self.widget)



    def mousePressEvent(self, event):
        self.clicked.emit(self.id)

