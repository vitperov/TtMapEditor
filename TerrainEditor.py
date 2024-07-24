#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.MapModelGeneral import *
from modules.Terrain.TerrainEditorView import *
from modules.Terrain.TerrainMapController import *
from modules.Terrain.Model import *

def main():
    app = QApplication(sys.argv)

    view = TerrainEditorView()
    view.show()
    
    model = Model()

    controller = TerrainMapController(view, model)

    exitcode = app.exec_()

    sys.exit(exitcode)

if __name__ == '__main__':
    main()
