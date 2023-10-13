#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.TerrainMapModel import *
from modules.Terrain.TerrainEditorView import *
from modules.Terrain.TerrainMapController import *
from modules.Terrain.TerrainGenerator import *

def main():
    app = QApplication(sys.argv)

    view = TerrainEditorView()
    view.show()

    model = TerrainMapModel()
    generator = TerrainGenerator(model)

    controller = TerrainMapController(view, model, generator)

    exitcode = app.exec_()

    sys.exit(exitcode)

if __name__ == '__main__':
    main()
