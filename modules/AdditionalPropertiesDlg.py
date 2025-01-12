from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from PyQt5 import QtGui
from modules.commonModels.ObjectsCollection import ObjectsCollection
from modules.commonModels.MapModelGeneral import MapObjectModelGeneral
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
    def __init__(self, name, type, value, texturesCollection, parent=None):
        super(TextureTypeWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        name_label = QLabel(f"Name: {name}")
        type_label = QLabel(f"Type: {type}")
        
        layout.addWidget(name_label)
        layout.addWidget(type_label)
        
        iconPath = texturesCollection.getIcon(value)
        icon_label = QLabel()
        if iconPath and os.path.exists(iconPath):
            pixmap = QtGui.QPixmap(iconPath)
        else:
            pixmap = QtGui.QPixmap()  # Empty pixmap if no valid icon path
        icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label)

class AdditionalPropertiesDlg(QDialog):
    def __init__(self, objCollection, mapObjectModel, texturesCollection, parent=None):
        super(AdditionalPropertiesDlg, self).__init__(parent)
        self.setWindowTitle("Additional Properties")
        
        self.texturesCollection = texturesCollection
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Get the model type from the map object model
        objType = mapObjectModel.getProperty('model')

        # Fetch additional properties for the object type
        additionalProps = objCollection.getAdditionalProperties(objType)

        # Display the properties in the GUI
        for prop in additionalProps:
            # Retrieve value from MapObjectModelGeneral if it exists
            propValue = mapObjectModel.additional_properties.get(prop.name, None)
            value_display = propValue.value if propValue else "Not Set"

            # Create a widget to show property name, type, and value
            if prop.type == "texture":
                widget = TextureTypeWidget(prop.name, prop.type, value_display, self.texturesCollection)
            else:
                widget = UnknownTypeWidget(prop.name, prop.type, value_display)
            layout.addWidget(widget)
