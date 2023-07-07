from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

class MapSettingsPanel(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        #self.widget = QGroupBox('Generator settings')

        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)

        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addStretch()
        mainLayout.addLayout(rightLayout)

        #self._generateBtn   = QPushButton("1")
        #self._saveBtn       = QPushButton("2")


        #--- Left

        areaLayout = QHBoxLayout()
        lbl1 = QLabel("Area size:")
        self.areaX = QLineEdit()
        lbl2 = QLabel("x")
        self.areaY = QLineEdit()
        areaLayout.addWidget(lbl1)
        areaLayout.addWidget(self.areaX)
        areaLayout.addWidget(lbl2)
        areaLayout.addWidget(self.areaY)
        areaLayout.addStretch()
        
        areaCntLayout = QHBoxLayout()
        lbla1 = QLabel("Rows:")
        self.areaRows = QLineEdit()
        lbla2 = QLabel("Columns:")
        self.areaColumns = QLineEdit()
        areaCntLayout.addWidget(lbla1)
        areaCntLayout.addWidget(self.areaRows)
        areaCntLayout.addWidget(lbla2)
        areaCntLayout.addWidget(self.areaColumns)
        areaCntLayout.addStretch()

        leftLayout.addLayout(areaLayout)
        leftLayout.addLayout(areaCntLayout)


        #---- Right
        
        #FIXME: wrap in function!
        houseProbLayout = QHBoxLayout()
        labHp = QLabel("House probability:")
        self.houseProbability = QLineEdit()
        houseProbLayout.addWidget(labHp)
        houseProbLayout.addWidget(self.houseProbability)

        shedProbLayout = QHBoxLayout()
        labSp = QLabel("Shed probability:")
        self.shedProbability = QLineEdit()
        shedProbLayout.addWidget(labSp)
        shedProbLayout.addWidget(self.shedProbability)
        
        
        treeProbLayout = QHBoxLayout()
        labTp = QLabel("Shed probability:")
        self.treeProbability = QLineEdit()
        treeProbLayout.addWidget(labTp)
        treeProbLayout.addWidget(self.treeProbability)

        rightLayout.addLayout(houseProbLayout)
        rightLayout.addLayout(shedProbLayout)
        rightLayout.addLayout(treeProbLayout)


        #self._layout.addStretch()

        #self._generateBtn.clicked.connect(self._newMap)
        #self._saveBtn.clicked.connect(self._saveFile)

