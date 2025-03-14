#!/usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize
import sys
import os

from modules.commonModels.MapModelGeneral import *
from modules.Terrain.TerrainEditorView import *
from modules.Terrain.TerrainMapController import *
from modules.Terrain.Model import *
from modules.House.HouseView import *
from modules.House.HouseController import *
from modules.commonModels.ObjectsCollection import *
from modules.commonModels.TexturesCollection import TexturesCollection
from modules.ApplicationSettings.ApplicationSettingsDlg import ApplicationSettingsDlg
from modules.ApplicationSettings.ApplicationSettingsModel import ApplicationSettingsModel

class TtMapEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TT Map Editor")
        
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        
        layout = QVBoxLayout()
        
        # Set a custom font with larger text size for the buttons
        buttonFont = QFont()
        buttonFont.setPointSize(24)  # Increase the font size as needed
        
        # Create Terrain Editor button with custom icon
        self.terrainButton = QPushButton("Terrain Editor")
        self.terrainButton.setFont(buttonFont)
        terrainIcon = QIcon("resources/terrainEditor.png")  # Load custom terrain icon
        self.terrainButton.setIcon(terrainIcon)
        self.terrainButton.setIconSize(QSize(150, 150))  # Set icon size
        self.terrainButton.setStyleSheet("padding-left: 20px;")  # Space between icon and text
        
        # Create House Editor button with custom icon
        self.houseButton = QPushButton("House Editor")
        self.houseButton.setFont(buttonFont)
        houseIcon = QIcon("resources/houseEditor.png")  # Load custom house icon
        self.houseButton.setIcon(houseIcon)
        self.houseButton.setIconSize(QSize(150, 150))  # Set icon size
        self.houseButton.setStyleSheet("padding-left: 20px;")  # Space between icon and text
        
        # Create Settings button with custom icon
        self.settingsButton = QPushButton("Settings")
        self.settingsButton.setFont(buttonFont)
        settingsIcon = QIcon("resources/settings.png")  # Load custom settings icon
        self.settingsButton.setIcon(settingsIcon)
        self.settingsButton.setIconSize(QSize(150, 150))  # Set icon size
        self.settingsButton.setStyleSheet("padding-left: 20px;")  # Space between icon and text
        
        # Add buttons to layout
        layout.addWidget(self.terrainButton)
        layout.addWidget(self.houseButton)
        layout.addWidget(self.settingsButton)
        
        self.centralWidget.setLayout(layout)
        
        # Connect button signals to their respective slots
        self.terrainButton.clicked.connect(self.showTerrainEditor)
        self.houseButton.clicked.connect(self.showHouseEditor)
        self.settingsButton.clicked.connect(self.showSettings)
        
        self.objCollection = None
        self.texturesCollection = None

    def showTerrainEditor(self):
        self.model = Model()
        view = TerrainEditorView()
        self.controller = TerrainMapController(view, self.model)
        self.setCentralWidget(view)
        
    def showHouseEditor(self):
        settings = ApplicationSettingsModel()
        nativeMapObjectsDir = os.path.join(os.path.dirname(__file__), 'mapObjects')
        externalMapObjectsDir = settings.getAdditionalMapObjectsDir()
        objCollection = ObjectsCollection([nativeMapObjectsDir, externalMapObjectsDir])

        nativeTexturesDir = os.path.join(os.path.dirname(__file__), 'textures')
        additionalTexturesDir = settings.getAdditionalTexturesDir()
        self.texturesCollection = TexturesCollection([nativeTexturesDir, additionalTexturesDir])
        
        self.model = MapModelGeneral(MapObjectModelGeneral, objCollection, self.texturesCollection)
        view = HouseView()
        self.controller = HouseController(view=view, houseModel=self.model)
        self.setCentralWidget(view)

    def showSettings(self):
        # Open the settings dialog
        settingsDialog = ApplicationSettingsDlg(self)
        if settingsDialog.exec_() == QDialog.Accepted:
            print("Settings saved successfully")

def main():
    app = QApplication(sys.argv)
    editor = TtMapEditor()
    editor.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
