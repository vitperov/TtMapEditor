from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from functools import partial

class GeneratorSettings(QWidget):
    def __init__(self, model):
        QWidget.__init__(self)
        self.model = model
        self.settings = {}
        self.controls = {}
        self.initGui()

    def initGui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        print("SCHEMA: " + str(self.model.schema))

        for key, info in self.model.schema.items():
            controlLayout = QHBoxLayout()
            label = QLabel(key)
            controlLayout.addWidget(label)

            settingType = info['type']
            settingValue = info['value']
            
            if settingType == 'str':
                control = QLineEdit()
                control.setText(settingValue)
            elif settingType == 'int':
                control = QSpinBox()
                control.setValue(int(settingValue))
            elif settingType == 'float':
                control = QDoubleSpinBox()
                control.setDecimals(2)
                control.setRange(-1e6, 1e6)  # Set an appropriate range for your needs
                control.setValue(float(settingValue))
            elif settingType == 'bool':
                control = QCheckBox()
                control.setChecked(int(settingValue))
            else:
                raise Exception("Unsupported schema type: " + settingType)
            
            controlLayout.addWidget(control)
            layout.addLayout(controlLayout)
            self.controls[key] = control

        appyButton = QPushButton("Appy")
        appyButton.clicked.connect(self.applySettings)
        layout.addWidget(appyButton)

    def applySettings(self):
        for key, control in self.controls.items():
            if isinstance(control, QLineEdit):
                self.settings[key]['value'] = control.text()
            elif isinstance(control, QSpinBox):
                self.settings[key]['value'] = control.value()
            elif isinstance(control, QDoubleSpinBox):
                self.settings[key]['value'] = control.value()
            elif isinstance(control, QCheckBox):
                self.settings[key]['value'] = control.isChecked()

class GeneratorItem(QWidget):
    def __init__(self, name, model):
        QWidget.__init__(self)
        self.name = name
        self.model = model;
        self.settings = {}
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        firstRowLayout = QHBoxLayout()
        settingsWg = GeneratorSettings(model)
        layout.addLayout(firstRowLayout)
        layout.addWidget(settingsWg)

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

