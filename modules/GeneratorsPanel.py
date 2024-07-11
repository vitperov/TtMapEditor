from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from functools import partial

class GeneratorItem(QWidget):
    def __init__(self, name, model):
        QWidget.__init__(self)
        self.name = name
        self.model = model;
        self.settings = {}
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        nameLabel = QLabel(name)
        layout.addWidget(nameLabel)
        
        generateBtn = QPushButton("Generate")
        layout.addWidget(generateBtn)
        generateBtn.clicked.connect(partial(model.generate, self.settings))

class GeneratorsPanel(QWidget):
    generateSignal = pyqtSignal(str, dict)
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
    
    def populateGenerators(self, generatorsModels):
        for name, model in generatorsModels.items():
            genItem = GeneratorItem(name, model);
            self.layout.addWidget(genItem)

