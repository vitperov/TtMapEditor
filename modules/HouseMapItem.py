from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

class HouseMapItem(QWidget):
    def __init__(self, id):
        #super().__init__(self)
        QWidget.__init__(self)
        
        self._id = id
        
        #self.grid = QGridLayout()
        #self.widget.setLayout(self.grid)
        self.widget = QtGui.QLabel(self)
        self.widget.setPixmap(QtGui.QPixmap("none.png"))
        self.widget.show() # ???
        #self.grid.addWidget(self.pic, 0, 0)
