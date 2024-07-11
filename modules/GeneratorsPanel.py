from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from functools import partial

class GeneratorItem(QWidget):
    generateSignal = pyqtSignal(str, dict)

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
        
    @pyqtSlot()
    def onGenerateClicked(self):
        self.generateSignal.emit(self.name, self.properties)


class GeneratorsPanel(QWidget):
    updatedEntireMap = pyqtSignal()
    generateSignal = pyqtSignal(str, dict)
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
    
    def populateGenerators(self, generatorsModels):
        for name, model in generatorsModels.items():
            genItem = GeneratorItem(name, model);
            self.layout.addWidget(genItem)
            genItem.generateSignal.connect(self.generateSignal)

