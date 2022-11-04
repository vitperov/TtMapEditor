from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

class HouseMapItem(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, id):
        QWidget.__init__(self)
        
        self.id = id
        self._model = None
        self._tilesize = 64
        
        size = QSize(self._tilesize, self._tilesize)
        
        self.widget = QtGui.QLabel(self)
        #self.widget = QtGui.QPushButton(self)
        
        pixmap = QtGui.QPixmap("resources/none.png")
        scaledPixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        self.widget.setPixmap(scaledPixmap)
        self.widget.setFixedSize(size)
        
        self.widget.setStyleSheet("background-color: lightgray")
        
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)
        
    def setModel(self, model):
        self._mode = model
        
    def updateState(self):
        print("Updating widget state")
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.id)

