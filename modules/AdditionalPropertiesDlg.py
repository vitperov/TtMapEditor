from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from modules.commonModels.ObjectsCollection import ObjectsCollection
from modules.commonModels.MapModelGeneral import MapObjectModelGeneral
from modules.ChooseTextureDlg import ChooseTextureDlg
import os


class UnknownTypeWidget(QWidget):
    def __init__(self, name, type, value, parent=None):
        super(UnknownTypeWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        name_label = QLabel(f"Name: {name}")
        type_label = QLabel(f"Type: {type}")
        value_label = QLabel(f"Value: {value}")
        
        layout.addWidget(name_label)
        layout.addWidget(type_label)
        layout.addWidget(value_label)


class TextureTypeWidget(QWidget):
    ICON_SIZE = 48

    def __init__(self, name, type, value, texturesCollection, mapModel, selectionRange, modelType, parent=None):
        super(TextureTypeWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        self.name = name
        self.type = type
        self.value = value
        self.texturesCollection = texturesCollection
        self.mapModel = mapModel
        self.selectionRange = selectionRange
        self.modelType = modelType

        name_label = QLabel(f"Name: {self.name}")
        type_label = QLabel(f"Type: {self.type}")
        
        layout.addWidget(name_label)
        layout.addWidget(type_label)
        
        iconPath = self.texturesCollection.getIcon(self.value)
        self.icon_button = QPushButton()
        if iconPath and os.path.exists(iconPath):
            pixmap = QtGui.QPixmap(iconPath)
        else:
            pixmap = self.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton).pixmap(self.ICON_SIZE, self.ICON_SIZE)
        pixmap = pixmap.scaled(self.ICON_SIZE, self.ICON_SIZE)
        self.icon_button.setIcon(QtGui.QIcon(pixmap))
        self.icon_button.setIconSize(QtCore.QSize(self.ICON_SIZE, self.ICON_SIZE))
        layout.addWidget(self.icon_button)

        self.icon_button.clicked.connect(self.on_icon_clicked)

    def on_icon_clicked(self):
        dlg = ChooseTextureDlg(self.texturesCollection, self)
        if dlg.exec_() == QDialog.Accepted:
            selected_texture = dlg.selectedTexture
            if selected_texture:
                self.mapModel.setGroupProperty(self.selectionRange, self.modelType, 'additionalProperties', {self.name: selected_texture})
                self.value = selected_texture
                self.update_icon()

    def update_icon(self):
        iconPath = self.texturesCollection.getIcon(self.value)
        if iconPath and os.path.exists(iconPath):
            pixmap = QtGui.QPixmap(iconPath)
        else:
            pixmap = self.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton).pixmap(self.ICON_SIZE, self.ICON_SIZE)
        pixmap = pixmap.scaled(self.ICON_SIZE, self.ICON_SIZE)
        self.icon_button.setIcon(QtGui.QIcon(pixmap))


class AdditionalPropertiesDlg(QDialog):
    def __init__(self, objCollection, mapModel, texturesCollection, selectionRange, modelType, parent=None):
        super(AdditionalPropertiesDlg, self).__init__(parent)
        self.setWindowTitle("Additional Properties")
        
        self.texturesCollection = texturesCollection
        self.mapModel = mapModel
        self.selectionRange = selectionRange
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        additionalProps = objCollection.getAdditionalProperties(modelType)

        for prop in additionalProps:
            selectedSquares = self.mapModel.getAllObjectOfType(modelType, self.selectionRange)
            propValue = None
            if selectedSquares:
                for square in selectedSquares:
                    for additional_prop in square.additional_properties:
                        if additional_prop.name == prop.name:
                            propValue = additional_prop.value
                            break
                    if propValue is not None:
                        break
            value_display = propValue if propValue else "Not Set"

            if prop.type == "texture":
                widget = TextureTypeWidget(prop.name, prop.type, value_display, self.texturesCollection, self.mapModel, self.selectionRange, modelType)
            else:
                widget = UnknownTypeWidget(prop.name, prop.type, value_display)
            layout.addWidget(widget)
