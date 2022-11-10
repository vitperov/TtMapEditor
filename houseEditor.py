#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.HouseModel import *
from modules.HouseView import *
from modules.HouseController import *

def main():
    app = QApplication(sys.argv)

    view = HouseView()
    view.show()

    model = HouseMapModel()

    controller = HouseController(view=view, houseModel=model)

    exitcode = app.exec_()

    sys.exit(exitcode)

if __name__ == '__main__':
    main()
