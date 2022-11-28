from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from modules.HouseMapItem import *

class HouseMapPanel(QWidget):
    activeItemChanged = pyqtSignal(int, int)

    def __init__(self):
        QWidget.__init__(self)
        self._layout = QGridLayout()
        self._model = None
        self.squares = dict()

        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setMargin(0);
        self._layout.setSpacing(0);

    def onItemClicked(self, x, y):
        print("Item clicked x=" + str(x) + "; y=" + str(y))
        self.activeItemChanged.emit(x, y)


    def setModel(self, model):
        self._model = model

    def redrawAll(self):
        [h, w] = self._model.size()

        for x in range(w):
            for y in range(h):
                widget = HouseMapSquare(x, y)
                self._layout.addWidget(widget, y, x)
                widget.clicked.connect(self.onItemClicked)
                key = (x, y)
                self.squares[key] = widget

        mapObjects = self._model.getAllSquares()
        for objectModel in mapObjects:
           x = objectModel.x
           y = objectModel.y
           square = self.squares[(x, y)]
           square.addItem(objectModel)
           objectModel.changed.connect(square.updateState)
           square.updateState()


        self._layout.setRowStretch(h, 1)
        self._layout.setColumnStretch(w, 1)
