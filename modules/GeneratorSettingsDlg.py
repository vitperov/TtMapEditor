from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

#import inspect
#from collections import namedtuple
import json
from json import JSONEncoder

from modules.GeneratorSettings import *

class GeneratorSettingsEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


def is_class(o):
    return hasattr(o, '__dict__')
    
class DynamicItem():
    def __init__(self, name, label, convertFunc, varStoragePtr):
        self._name = name
        self._label = label
        self._layout = None
        self._convertFunc = convertFunc

        self._editWg = None
        
        self._varStoragePtr = varStoragePtr

        self._createLayout()

    def _createLayout(self):
        self._layout = QHBoxLayout()
        label = QLabel(self._label)
        self._editWg = QLineEdit()
        self._layout.addWidget(label)
        self._layout.addWidget(self._editWg)
        val = getattr(self._varStoragePtr, self._name)
        self._editWg.setText(str(val))

    def getLayout(self):
        return self._layout


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
        
        self.dynamicLayout = QVBoxLayout()
        layout.addLayout(self.dynamicLayout)

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

    def createControlsByClassVariables(self, var, prefix, layout):
        for attr in dir(var):
            if attr.startswith("__"):
                continue
            val = getattr(var, attr)
            if callable(val):
                continue

            if is_class(val):
                print(prefix + attr + "->");
                nestedLayout = QVBoxLayout()
                box = QGroupBox(attr)
                box.setLayout(nestedLayout)
                #layout.addLayout(nestedLayout)
                layout.addWidget(box)
                self.createControlsByClassVariables(val, prefix + "    ", nestedLayout)
                continue

            print(prefix + attr + "->" + str(val))
            item = DynamicItem(attr, attr, type(val), var)
            layout.addLayout(item.getLayout())


    def onSavePressed(self):
        self.saveToFile('testSettings.json')


    def onLoadPressed(self):
        self.loadFromFile('testSettings.json')
        print(self.settings.__dict__)
        print(self.settings.zoneSettings.__dict__)
        print("----------")
        self.createControlsByClassVariables(self.settings, "", self.dynamicLayout)


    @staticmethod
    def runDlg():
        dlg = GeneratorSettingsDlg()
        dlg.setModal(True)
        dlg.exec_()

