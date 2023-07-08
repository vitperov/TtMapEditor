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
        lbl1 = QLabel("Area size W:")
        self.areaW = QLineEdit()
        lbl2 = QLabel(" H:")
        self.areaH = QLineEdit()
        areaLayout.addWidget(lbl1)
        areaLayout.addWidget(self.areaW)
        areaLayout.addWidget(lbl2)
        areaLayout.addWidget(self.areaH)
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

    def setValues(self, s):
        self.areaW.setText(           str(s['areaW']))
        self.areaH.setText(           str(s['areaH']))
        self.areaRows.setText(        str(s['areaRows']))
        self.areaColumns.setText(     str(s['areaColumns']))
        self.houseProbability.setText(str(s['houseProbability']))
        self.shedProbability.setText( str(s['shedProbability']))
        self.treeProbability.setText( str(s['treeProbability']))

    def getValues(self):
        s = dict()
        s['areaW']              = int(self.areaW.text())
        s['areaH']              = int(self.areaH.text())
        s['areaRows']           = int(self.areaRows.text())
        s['areaColumns']        = int(self.areaColumns.text())
        s['houseProbability']   = float(self.houseProbability.text())
        s['shedProbability']    = float(self.shedProbability.text())
        s['treeProbability']    = float(self.treeProbability.text())

        return s

