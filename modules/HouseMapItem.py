from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

from modules.HouseModel import *

def rotIdToAngle(rotStr):
    return int(rotStr);


class HouseMapSquare(QWidget):
    clicked = pyqtSignal(int, int)

    def __init__(self, x, y):
        QWidget.__init__(self)

        self.x = x
        self.y = y

        self.items = list()

        self._tilesize = 64
        self.size = QSize(self._tilesize, self._tilesize)

        self.widget = QtGui.QLabel(self)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self.widget)
        self._layout.setContentsMargins(0,0,0,0)

        self.setLayout(self._layout)

        self.updateState()

    def updateState(self):
        combinedPixmap = QtGui.QPixmap(self.size)

        self.widget.setParent(None)
        self.widget = QtGui.QLabel(self)

        painter = QtGui.QPainter(combinedPixmap)
        painter.fillRect(QRect(0, 0, self.size.width(), self.size.height()), QtGui.QBrush(QtGui.QColor("lightgray")));
        for item in self.items:
            #print("Getting pixmap: " + str(self.x) + ", " + str(self.y))
            pm = item.getPixmap(self.size)
            painter.drawPixmap(QtCore.QRectF(pm.rect()), pm, QtCore.QRectF(pm.rect()))

        del painter

        self.widget.setPixmap(combinedPixmap)
        self.widget.setFixedSize(self.size)

        #self.widget.setStyleSheet("background-color: lightgray")
        self._layout.addWidget(self.widget)


    def addItem(self, model, objCollection):
        item = HouseMapItem(model, objCollection)
        self.items.append(item)

    def mousePressEvent(self, event):
        self.clicked.emit(self.x, self.y)

class HouseMapItem():
    def __init__(self, model, objCollection):
        self._model = model
        self._objCollection = objCollection

    def getPixmap(self, size):
        sqType      = self._model.getProperty('model')
        rotation    = self._model.getProperty('rotation')
        
        imgFile = self._objCollection.getIcon(sqType)

        pixmap = QtGui.QPixmap(imgFile)
        transform = QtGui.QTransform().rotate(rotIdToAngle(rotation))

        rotatedPixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        scaledPixmap = rotatedPixmap.scaled(size, QtCore.Qt.KeepAspectRatio)

        return scaledPixmap


