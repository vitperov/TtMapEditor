from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import json
from json import JSONEncoder

from modules.GeneratorSettings       import *
from modules.ClassVariablesGuiEditor import *

class GeneratorSettingsEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


class GeneratorSettingsDlg(QtGui.QDialog):
    def __init__(self):
        super().__init__()

        self.settings = GeneratorSettings()

        self.setWindowTitle("Terrain generator settings")

        layout = QVBoxLayout()

        loadSaveLayout = QHBoxLayout()

        loadButton = QPushButton()
        saveButton = QPushButton()

        loadButton.setText("Load settings")
        saveButton.setText("Save settings")

        loadButton.clicked.connect(self.onLoadPressed)
        saveButton.clicked.connect(self.onSavePressed)

        loadSaveLayout.addWidget(loadButton)
        loadSaveLayout.addWidget(saveButton)

        layout.addLayout(loadSaveLayout)

        self.dynamicLayout = QVBoxLayout()
        layout.addLayout(self.dynamicLayout)

        self.setLayout(layout)


    def saveToFile(self, filename):
        extension = '.json'
        if not filename.endswith(extension):
            filename = filename + extension

        print("Saving settings to " + filename)
        with open(filename, "w+") as writeFile:
            jsonObj = json.dumps(self.settings, indent=4, cls=GeneratorSettingsEncoder)
            writeFile.write(jsonObj)

    def loadFromFile(self, filename):
        extension = '.json'
        if not filename.endswith(extension):
            filename = filename + extension

        print("Loading map to " + filename)

        with open(filename, "r") as readFile:
            jsStr = readFile.read()
            settingsDict = json.loads(jsStr)
            self.settings.loadFromDict(settingsDict)

    def onSavePressed(self):
        self.saveToFile('testSettings.json')


    def onLoadPressed(self):
        self.loadFromFile('testSettings.json')
        #print(self.settings.__dict__)
        #print(self.settings.zoneSettings.__dict__)
        #print("----------")
        edt = ClassVariablesGuiEditor();
        edt.createControls(self.settings, "", self.dynamicLayout)


    @staticmethod
    def runDlg():
        dlg = GeneratorSettingsDlg()
        dlg.setModal(True)
        dlg.exec_()

