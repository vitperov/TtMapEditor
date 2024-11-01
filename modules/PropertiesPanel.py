from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from functools import partial

class SimpleSquareItem(QWidget):
    def __init__(self, model, objCollection, tilesize):
        super(SimpleSquareItem, self).__init__()
        self._model = model
        self._objCollection = objCollection
        self._tilesize = tilesize
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        label = QLabel()
        self.updatePixmap(label)
        
        layout.addWidget(label)
    
    def updatePixmap(self, label):
        sqType = self._model.getProperty('model')
        rotation = self._model.getProperty('rotation')

        imgFile = self._objCollection.getIcon(sqType)
        try:
            pixmap = QtGui.QPixmap(imgFile, "1")
        except:
            pixmap = QtGui.QPixmap(imgFile)
        
        transform = QtGui.QTransform().rotate(int(rotation))
        rotatedPixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        
        size = QSize(self._tilesize, self._tilesize)
        scaledPixmap = rotatedPixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        
        label.setPixmap(scaledPixmap)

#FIXME turn to widget. Possible memory leak
class PropertiesItem():
    def __init__(self, objModel, title, objCollection, mapModel, category, tilesize=64):
        self._model = objModel
        self._mapModel = mapModel

        self.widget = QGroupBox(title)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        # Add SimpleSquareItem before properties
        self.simpleSquareItem = SimpleSquareItem(objModel, objCollection, tilesize)
        self.layout.addWidget(self.simpleSquareItem)

        availableObjects = objCollection.getTypesInCategory(category)

        def addBoxParameter(propName, propValue, possibleValues):
            groupbox = QGroupBox(propName)
            self.layout.addWidget(groupbox)
            box = QVBoxLayout()
            groupbox.setLayout(box)

            valType = type(propValue)
            print(valType)
            if valType == 'Enum':
                nValues = len(valType)
            else:
                nValues = len(availableObjects) 
            
            comboBox = QComboBox()
            for optionName in possibleValues:
                comboBox.addItem(optionName, optionName)
            
            comboBox.setCurrentIndex(possibleValues.index(propValue))
            box.addWidget(comboBox)
            
            def onIndexChanged(propName, valueIdx):
                valueStr = possibleValues[valueIdx]
                self._model.setProperty(propName, valueStr)
                self._mapModel.updateEntireMap()

            comboBox.currentIndexChanged.connect(partial(onIndexChanged, propName))

        addBoxParameter('model',    self._model.properties['model'], availableObjects)
        addBoxParameter('rotation', self._model.properties['rotation'], list(self._model.classnames['rotation']))

class PropertiesPanel(QWidget):
    updatedEntireMap = pyqtSignal()
    def __init__(self, category):
        QWidget.__init__(self)

        self.x = None
        self.y = None
        self.zLevel = None
        self._category = category

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.coordinatesLbl = QLabel("X: ? Y: ?")
        layout.addWidget(self.coordinatesLbl)

        self.properties = QVBoxLayout()
        layout.addLayout(self.properties)

        addBtn = QPushButton("Add object")
        layout.addWidget(addBtn)
        addBtn.clicked.connect(self.addObject)

    def setModel(self, model):
        self.mapModel = model

    def showSquareProperties(self, x, y, z):
        self.x = x
        self.y = y
        self.zLevel = z

        for i in reversed(range(self.properties.count())):
            self.properties.itemAt(i).widget().setParent(None)

        items = self.mapModel.getSquareItems(x, y, z)
        num = 0;
        for itemModel in items:
            self.coordinatesLbl.setText("X: " + str(x) + " Y: " + str(y) + " Zlevel: " + str(z))

            num += 1;
            title = str(num)
            itemWg = PropertiesItem(itemModel, title, self.mapModel._objCollection, self.mapModel, self._category)
            self.properties.addWidget(itemWg.widget)

            removeBtn = QPushButton("Remove")
            self.properties.addWidget(removeBtn)

            removeBtn.clicked.connect(partial(self.removeObject, itemModel.id))

    def addObject(self):
        if self.x is not None and self.y is not None and self.zLevel is not None:
            obj = self.mapModel.createObjectAt(self.x, self.y, self.zLevel)
            self.showSquareProperties(self.x, self.y, self.zLevel)
            self.updatedEntireMap.emit()

    def removeObject(self, id):
        self.mapModel.deleteSquareById(id)
        self.showSquareProperties(self.x, self.y)
