#!/usr/bin/python

from PyQt5.QtWidgets import *
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
        
        self.terrainButton = QPushButton("Terrain Editor")
        self.houseButton = QPushButton("House Editor")
        
        layout.addWidget(self.terrainButton)
        layout.addWidget(self.houseButton)
        
        self.centralWidget.setLayout(layout)
        
        self.terrainButton.clicked.connect(self.showTerrainEditor)
        self.houseButton.clicked.connect(self.showHouseEditor)
        
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

def main():
    app = QApplication(sys.argv)
    editor = TtMapEditor()
    editor.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
