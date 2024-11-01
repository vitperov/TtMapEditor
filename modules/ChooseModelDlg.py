from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize
from functools import partial

class ChooseModelDlg(QDialog):
    def __init__(self, objCollection, category, tilesize, parent=None):
        super(ChooseModelDlg, self).__init__(parent)
        self.setWindowTitle("Choose Model")
        self.selectedModel = None
        self._tilesize = tilesize
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        availableObjects = objCollection.getTypesInCategory(category)
        
        col_count = 4
        for index, model in enumerate(availableObjects):
            row = index // col_count
            col = index % col_count
            
            itemLayout = QVBoxLayout()
            
            label = QLabel(f"{model}")
            itemLayout.addWidget(label)
            
            btn = QPushButton()
            self.updatePixmap(btn, objCollection, model)
            btn.clicked.connect(partial(self.onButtonClicked, model))
            itemLayout.addWidget(btn)
            
            layout.addLayout(itemLayout, row, col)
    
    def updatePixmap(self, button, objCollection, model):
        imgFile = objCollection.getIcon(model)
        try:
            pixmap = QtGui.QPixmap(imgFile, "1")
        except:
            pixmap = QtGui.QPixmap(imgFile)
        
        size = QSize(self._tilesize, self._tilesize)
        scaledPixmap = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        
        button.setIcon(QtGui.QIcon(scaledPixmap))
        button.setIconSize(size)

    def onButtonClicked(self, model):
        self.selectedModel = model
        self.accept()
