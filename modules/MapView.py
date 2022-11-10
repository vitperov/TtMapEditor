from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import numpy
import random

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.HouseMapPanel import *
from modules.PropertiesPanel import *
from modules.MapActionsPanel import *


class MapView(QMainWindow):
    """Main Window."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TT Map Generator')

        self._createWidgets()

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self._createLayout())

    def _createWidgets(self):
        self.actionsPanel = MapActionsPanel()

    def _createLayout(self):
        layout = QVBoxLayout()

        layout.addWidget(self.actionsPanel)

        return layout

