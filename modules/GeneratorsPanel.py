from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from functools import partial

class GeneratorItem(QWidget):
    generateSignal = pyqtSignal(str, dict)

    def __init__(self, name):
        QWidget.__init__(self)
        self.name = name;
        self.properties = {}
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        nameLabel = QLabel(name)
        layout.addWidget(nameLabel)
        
        generateBtn = QPushButton("Generate")
        layout.addWidget(generateBtn)
        generateBtn.clicked.connect(self.onGenerateClicked)
        
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
    
    def populateGenerators(self, names):
        for generatorName in names:
            genItem = GeneratorItem(generatorName);
            self.layout.addWidget(genItem)
            genItem.generateSignal.connect(self.generateSignal)

