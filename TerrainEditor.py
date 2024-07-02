#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.MapModelGeneral import *
from modules.Terrain.TerrainEditorView import *
from modules.Terrain.TerrainMapController import *
from modules.Terrain.TerrainGenerator import *
from modules.ObjectsCollection import *

from modules.GeneratorPluginsLoader import *

def main():
    app = QApplication(sys.argv)
    
    nativeMapObjectsDir   = os.path.join(os.path.dirname(__file__), 'mapObjects/native')
    externalMapObjectsDir = os.path.join(os.path.dirname(__file__), 'mapObjects/external')
    objCollection = ObjectsCollection([nativeMapObjectsDir, externalMapObjectsDir])
    print("Map objects found: " + str(objCollection.allObjectTypes()))

    pluginsDir = os.path.join(os.path.dirname(__file__), 'generators')
    generators = GeneratorPluginsLoader()
    generators.loadPluginsFrom(pluginsDir)
    print("Generator plugins found: " + str(generators.generators))

    view = TerrainEditorView()
    view.show()

    model = MapModelGeneral(MapObjectModelGeneral, objCollection)
    generator = TerrainGenerator(model)

    controller = TerrainMapController(view, model, generator)

    exitcode = app.exec_()

    sys.exit(exitcode)

if __name__ == '__main__':
    main()
