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

    def __init__(self, name, type, value, texturesCollection, mapObjectModel, parent=None):
        super(TextureTypeWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        self.name = name
        self.type = type
        self.value = value
        self.texturesCollection = texturesCollection
        self.mapObjectModel = mapObjectModel

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
                self.value = selected_texture
                self.mapObjectModel.setAdditioanalProperty(self.name, self.value)
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
    def __init__(self, objCollection, mapObjectModel, texturesCollection, parent=None):
        super(AdditionalPropertiesDlg, self).__init__(parent)
        self.setWindowTitle("Additional Properties")
        
        self.texturesCollection = texturesCollection
        self.mapObjectModel = mapObjectModel
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Get the model type from the map object model
        objType = mapObjectModel.getProperty('model')

        # Fetch additional properties for the object type
        additionalProps = objCollection.getAdditionalProperties(objType)

        # Display the properties in the GUI
        for prop in additionalProps:
            # Retrieve value from MapObjectModelGeneral if it exists
            propValue = next((p for p in mapObjectModel.additional_properties if p.name == prop.name), None)
            value_display = propValue.value if propValue else "Not Set"

            # Create a widget to show property name, type, and value
            if prop.type == "texture":
                widget = TextureTypeWidget(prop.name, prop.type, value_display, self.texturesCollection, self.mapObjectModel)
            else:
                widget = UnknownTypeWidget(prop.name, prop.type, value_display)
            layout.addWidget(widget)
