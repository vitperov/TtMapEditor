#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize
import sys
import os

from modules.MapModelGeneral import *
from modules.Terrain.TerrainEditorView import *
from modules.Terrain.TerrainMapController import *
from modules.Terrain.Model import *
from modules.House.HouseView import *
from modules.House.HouseController import *
from modules.ObjectsCollection import *

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

    def showTerrainEditor(self):
        model = Model()
        view = TerrainEditorView()
        controller = TerrainMapController(view, model)
        self.setCentralWidget(view)
        
    def showHouseEditor(self):
        if not self.objCollection:  # Lazy loading of objects collection
            nativeMapObjectsDir = os.path.join(os.path.dirname(__file__), 'mapObjects/native')
            externalMapObjectsDir = os.path.join(os.path.dirname(__file__), 'mapObjects/external')
            self.objCollection = ObjectsCollection([nativeMapObjectsDir, externalMapObjectsDir])
        
        model = MapModelGeneral(MapObjectModelGeneral, self.objCollection)
        view = HouseView()
        controller = HouseController(view=view, houseModel=model)
        self.setCentralWidget(view)
    
    def showSettings(self):
        # Placeholder for settings functionality
        settingsDialog = QDialog(self)
        settingsDialog.setWindowTitle("Settings")
        settingsDialog.setModal(True)
        settingsDialog.exec_()

def main():
    app = QApplication(sys.argv)
    editor = TtMapEditor()
    editor.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
