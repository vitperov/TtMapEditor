#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.Terrain.TerrainMapModel import *
from modules.Terrain.TerrainEditorView import *
from modules.Terrain.TerrainMapController import *
from modules.Terrain.TerrainGenerator import *
from modules.ObjectsCollection import *

def main():
    app = QApplication(sys.argv)
    
    nativeMapObjectsDir   = os.path.join(os.path.dirname(__file__), 'mapObjects/native')
    externalMapObjectsDir = os.path.join(os.path.dirname(__file__), 'mapObjects/external')
    objCollection = ObjectsCollection([nativeMapObjectsDir, externalMapObjectsDir])
    print("Map objects found: " + str(objCollection.allObjectTypes()))

    view = TerrainEditorView()
    view.show()

    model = TerrainMapModel(objCollection)
    generator = TerrainGenerator(model)

    controller = TerrainMapController(view, model, generator)

    exitcode = app.exec_()

    sys.exit(exitcode)

if __name__ == '__main__':
    main()
