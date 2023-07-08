from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

class ParamItemSingle():
    def __init__(self, name, label, convertFunc):
        self._name = name
        self._label = label
        self._layout = None
        self._convertFunc = convertFunc

        self._editWg = None

        self._createLayout()

    def _createLayout(self):
        self._layout = QHBoxLayout()
        label = QLabel(self._label)
        self._editWg = QLineEdit()
        self._layout.addWidget(label)
        self._layout.addWidget(self._editWg)

    def getLayout(self):
        return self._layout

    def saveToDict(self, d):
        d[self._name] = self._convertFunc(self._editWg.text())

    def loadFromDict(self, d):
        self._editWg.setText(str(d[self._name]))

class MapSettingsPanel(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)

        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addStretch()
        mainLayout.addLayout(rightLayout)

        self.allItems = []

        #--- Left

        areaW = ParamItemSingle('areaW', "Area Width:", int)
        areaH = ParamItemSingle('areaH', "Height:"    , int)
        areaSzLayout = QHBoxLayout()
        areaSzLayout.addLayout(areaW.getLayout())
        areaSzLayout.addLayout(areaH.getLayout())

        areaRows    = ParamItemSingle('areaRows',    "Area Width:", int)
        areaColumns = ParamItemSingle('areaColumns', "Height:",     int)
        areaCntLayout = QHBoxLayout()
        areaCntLayout.addLayout(areaRows.getLayout())
        areaCntLayout.addLayout(areaColumns.getLayout())

        self.allItems.append(areaW)
        self.allItems.append(areaH)
        self.allItems.append(areaRows)
        self.allItems.append(areaColumns)

        leftLayout.addLayout(areaSzLayout)
        leftLayout.addLayout(areaCntLayout)


        #---- Right

        houseProb        = ParamItemSingle('houseProbability', "House probability:",        float)
        shedProb         = ParamItemSingle('shedProbability',  "Shed probability:",         float)
        treeProb         = ParamItemSingle('treeProbability',  "Tree probability:",         float)
        forestKeepOut    = ParamItemSingle('forestKeepOut',    "Tree rows around the map:", int)

        self.allItems.append(houseProb)
        self.allItems.append(shedProb)
        self.allItems.append(treeProb)
        self.allItems.append(forestKeepOut)

        rightLayout.addLayout(houseProb.getLayout())
        rightLayout.addLayout(shedProb.getLayout())
        rightLayout.addLayout(treeProb.getLayout())
        rightLayout.addLayout(forestKeepOut.getLayout())

    def setValues(self, s):
        for item in self.allItems:
            item.loadFromDict(s)

    def getValues(self):
        s = dict()
        for item in self.allItems:
            item.saveToDict(s)

        return s

