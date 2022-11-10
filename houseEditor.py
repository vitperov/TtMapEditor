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
    
    #stream = Stream(newText=view.consoleWrite)
    #sys.stdout = stream
        

    model = HouseMapModel()
    #model.initMap(5, 6)

    controller = HouseController(view=view, houseModel=model)

    exitcode = app.exec_()
    
    #del stream
    sys.stdout = sys.__stdout__

    sys.exit(exitcode)

if __name__ == '__main__':
    main()
