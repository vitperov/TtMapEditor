from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

from modules.MapItem import *

class MapWidget(QWidget):
    activeItemChanged = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        self._layout = QGridLayout()
        #self._items = {}
        self._model = None

        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setMargin(0);
        self._layout.setSpacing(0);

    def onItemClicked(self, itemId):
        print("Item clicked Id=" + str(itemId))
        self.activeItemChanged.emit(itemId)


    def setModel(self, model):
        self._model = model
        
    def redrawAll(self):
        [h, w] = self._model.size()
        mapSquares = self._model.getAllSquares().items()

        for id, squareModel in mapSquares:
            [x, y] = squareModel.getXY()
            widget = MapItem(squareModel)
            self._layout.addWidget(widget, y, x)
            #widget.setModel(squareModel)
            widget.clicked.connect(self.onItemClicked)
            squareModel.changed.connect(widget.updateState)
            
        self._layout.setRowStretch(h, 1)
        self._layout.setColumnStretch(w, 1)
