#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.MapModel import *
from modules.MapView import *
from modules.MapController import *

def main():
    app = QApplication(sys.argv)

    view = MapView()
    view.show()

    model = MapModel()

    controller = MapController(view=view, mapModel=model)

    exitcode = app.exec_()

    sys.exit(exitcode)

if __name__ == '__main__':
    main()