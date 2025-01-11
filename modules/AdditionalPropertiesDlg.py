from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from modules.commonModels.ObjectsCollection import ObjectsCollection
from modules.commonModels.MapModelGeneral import MapObjectModelGeneral

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
    def __init__(self, name, type, value, parent=None):
        super(TextureTypeWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        name_label = QLabel(f"Name: {name}")
        type_label = QLabel(f"Type: {type}")
        value_label = QLabel(f"Value: {value}")
        
        layout.addWidget(name_label)
        layout.addWidget(type_label)
        layout.addWidget(value_label)

class AdditionalPropertiesDlg(QDialog):
    def __init__(self, objCollection, mapObjectModel, parent=None):
        super(AdditionalPropertiesDlg, self).__init__(parent)
        self.setWindowTitle("Additional Properties")
        
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
            if objType == "texture":
                widget = TextureTypeWidget(prop.name, prop.type, value_display)
            else:
                widget = UnknownTypeWidget(prop.name, prop.type, value_display)
            layout.addWidget(widget)
