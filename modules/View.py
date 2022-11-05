from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import numpy
import random

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.HouseMapPanel import *
from modules.PropertiesPanel import *
from modules.ActionsPanel import *


class Window(QMainWindow):
    """Main Window."""
    def __init__(self):
        """Initializer."""
        super().__init__()
        self.setWindowTitle('TT Map editor')
        
        self._createWidgets()

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self._createLayout())
        
    def _createWidgets(self):
        self.houseMapPanel = HouseMapPanel(5, 5)
        self.propPanel = PropertiesPanel()
        self.actionsPanel = ActionsPanel() 

    def _createLayout(self):
        layout = QVBoxLayout()
        
        layout.addWidget(self.actionsPanel)
        mapLayout = QHBoxLayout()
        layout.addLayout(mapLayout)

        mapLayout.addWidget(self.houseMapPanel)
        mapLayout.addWidget(self.propPanel)

        return layout

