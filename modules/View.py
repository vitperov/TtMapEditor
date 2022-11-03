from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import numpy
import random

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.HouseMapPanel import *
from modules.PropertiesPanel import *


class Window(QMainWindow):
    """Main Window."""
    def __init__(self):
        """Initializer."""
        super().__init__()
        self.setWindowTitle('TT Map editor')

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self._createLayout())

    def _createLayout(self):
        layout = QGridLayout()

        self.houseMapPanel = HouseMapPanel(5, 5)
        self.propPanel = PropertiesPanel()
        
        layout.addWidget(self.houseMapPanel, 0, 0)
        layout.addWidget(self.propPanel, 0, 1)

        return layout

