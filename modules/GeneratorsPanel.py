from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

class GeneratorItem(QWidget):
    def __init__(self, name):
        QWidget.__init__(self)
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        nameLabel = QLabel(name)
        layout.addWidget(nameLabel)
        
        generateBtn = QPushButton("Generate")
        layout.addWidget(generateBtn)


class GeneratorsPanel(QWidget):
    updatedEntireMap = pyqtSignal()
    def __init__(self):
        QWidget.__init__(self)

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        generators = ["Empty", "Trees outline", "Road", "Buildings", "Fog", "Opponent respawns", "Berries"]
        
        for generatorName in generators:
            genItem = GeneratorItem(generatorName);
            layout.addWidget(genItem)


