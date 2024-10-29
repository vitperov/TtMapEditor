from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from modules.ApplicationSettings.ApplicationSettingsModel import ApplicationSettingsModel

class ApplicationSettingsDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Application settings")
        self.setModal(True)
        
        # Initialize settings model within the dialog
        self.settingsModel = ApplicationSettingsModel()

        # Layout for the dialog
        layout = QVBoxLayout()

        # Input for additionalMapObjectsDir
        self.mapObjectsDirLabel = QLabel("Additional Map Objects Directory:")
        self.mapObjectsDirInput = QLineEdit()
        self.mapObjectsDirInput.setText(self.settingsModel.getAdditionalMapObjectsDir())  # Load existing value
        layout.addWidget(self.mapObjectsDirLabel)
        layout.addWidget(self.mapObjectsDirInput)

        # Input for additionalGeneratorsDir
        self.generatorsDirLabel = QLabel("Additional Generators Directory:")
        self.generatorsDirInput = QLineEdit()
        self.generatorsDirInput.setText(self.settingsModel.getAdditionalGeneratorsDir())  # Load existing value
        layout.addWidget(self.generatorsDirLabel)
        layout.addWidget(self.generatorsDirInput)

        # Save button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()  # Push button to the right
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveSettings)  # Connect to save action
        buttonLayout.addWidget(self.saveButton)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def saveSettings(self):
        # Update settings model with new values
        self.settingsModel.setAdditionalMapObjectsDir(self.mapObjectsDirInput.text())
        self.settingsModel.setAdditionalGeneratorsDir(self.generatorsDirInput.text())
        self.accept()  # Close dialog after saving
