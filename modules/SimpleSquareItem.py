from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from pyqtgraph.Qt import QtCore

class SimpleSquareItem(QWidget):
    def __init__(self, model, objCollection, tilesize):
        super(SimpleSquareItem, self).__init__()
        self._model = model
        self._objCollection = objCollection
        self._tilesize = tilesize
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        label = QLabel()
        self.updatePixmap(label)
        
        layout.addWidget(label)
    
    def updatePixmap(self, label):
        sqType = self._model.getProperty('model')
        rotation = self._model.getProperty('rotation')

        imgFile = self._objCollection.getIcon(sqType)
        try:
            pixmap = QtGui.QPixmap(imgFile, "1")
        except:
            pixmap = QtGui.QPixmap(imgFile)
        
        transform = QtGui.QTransform().rotate(int(rotation))
        rotatedPixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        
        size = QSize(self._tilesize, self._tilesize)
        scaledPixmap = rotatedPixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        
        label.setPixmap(scaledPixmap)
