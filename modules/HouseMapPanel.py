from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

from modules.HouseMapItem import *

class HouseMapPanel(QWidget):
    activeItemChanged = pyqtSignal(int)

    def __init__(self, height, width):
        QWidget.__init__(self)
        self._layout = QGridLayout()
        #self._items = {}
        self._model = None

        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setMargin(0);
        self._layout.setSpacing(0);

        self._layout.setRowStretch(height, 1)
        self._layout.setColumnStretch(width, 1)

    def onItemClicked(self, itemId):
        print("Item clicked Id=" + str(itemId))
        self.activeItemChanged.emit(itemId)


    def setModel(self, model):
        self._model = model
        [h, w] = self._model.size()
        mapSquares = self._model.getAllSquares().items()

        for id, squareModel in mapSquares:
            [x, y] = squareModel.getXY()
            widget = HouseMapItem(squareModel)
            self._layout.addWidget(widget, y, x)
            #widget.setModel(squareModel)
            widget.clicked.connect(self.onItemClicked)
            squareModel.changed.connect(widget.updateState)
