from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def is_class(o):
    return hasattr(o, '__dict__')

class ClassVariablesGuiEditor():
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

            def onTextChanged(txt):
                try:
                    value = self._convertFunc(txt)
                    setattr(self._varStoragePtr, self._name, value)
                except:
                    pass

            self._editWg.textChanged.connect(onTextChanged)

        def getLayout(self):
            return self._layout

    # NOTE: we do not store anything iside the class, but let it be
    # the class method insted of just functin (perhaps we will need it in the future)

    def createControls(self, cls, layout):
        for attr in dir(cls):
            if attr.startswith("__"):
                continue
            if attr.startswith("_"):
                continue

            val = getattr(cls, attr)
            if callable(val):
                continue

            if isinstance(val, list):
                listLayout = QVBoxLayout()
                box = QGroupBox(attr)
                box.setLayout(listLayout)
                layout.addWidget(box)
                for itemId in range(len(val)):
                    itemLayout = QVBoxLayout()
                    itemBox = QGroupBox(str(itemId+1))
                    itemBox.setLayout(itemLayout)
                    listLayout.addWidget(itemBox)
                    item = val[itemId]
                    self.createControls(item, itemLayout)

                continue

            if is_class(val):
                print(attr + "-> class");
                nestedLayout = QVBoxLayout()
                box = QGroupBox(attr)
                box.setLayout(nestedLayout)
                layout.addWidget(box)
                #print("Adding class control: " + str(val))
                self.createControls(val, nestedLayout)
                continue

            #print(attr + "->" + str(val))
            item = self.DynamicItem(attr, attr, type(val), cls)
            layout.addLayout(item.getLayout())
