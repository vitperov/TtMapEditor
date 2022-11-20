#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.TerrainMapModel import *
from modules.MapView import *
from modules.MapController import *
from modules.MapGenerator import *

def main():
    app = QApplication(sys.argv)

    view = MapView()
    view.show()

    model = TerrainMapModel()
    generator = MapGenerator(model)

    controller = MapController(view, model, generator)

    exitcode = app.exec_()

    sys.exit(exitcode)

if __name__ == '__main__':
    main()
