from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

#from collections import namedtuple
import json
from json import JSONEncoder

from modules.GeneratorSettings import *

class GeneratorSettingsEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

#def GeneratorSettingsDecoder(inputDict):
#    return namedtuple('X', inputDict.keys())(*inputDict.values())

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
        
        #label = QLabel('Do not forget to push "Save" on the main window')
        #layout.addWidget(label)
        #label.setStyleSheet("QLabel { color : red; qproperty-alignment: AlignCenter;}");
        
        #varNames = ['calibration', 'speed20ma', 'amplitude20ma']
        #panel = VariablesPanelWidget()
        #panel.populateModelVariables(model, varNames)
        #layout.addWidget(panel)
        
        self.setLayout(layout)


    def saveToFile(self, filename):
        extension = '.json'
        if not filename.endswith(extension):
            filename = filename + extension

        print("Saving settings to " + filename)
        with open(filename, "w") as writeFile:
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
        print(self.settings.__dict__)
        print(self.settings.zoneSettings.__dict__)


    @staticmethod
    def runDlg():
        dlg = GeneratorSettingsDlg()
        dlg.setModal(True)
        dlg.exec_()

