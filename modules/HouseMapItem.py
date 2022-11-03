from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui

class HouseMapItem(QWidget):
    def __init__(self, id):
        QWidget.__init__(self)
        
        self._id = id
        
        self.widget = QtGui.QLabel(self)
        self.widget.setPixmap(QtGui.QPixmap("none.png"))
        #self.widget.show() # ???
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        self.setLayout(layout)
