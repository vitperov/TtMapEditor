#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modules.MapModelGeneral import *
from modules.HouseView import *
from modules.HouseController import *
from modules.ObjectsCollection import *

def main():
    app = QApplication(sys.argv)
    
    nativeMapObjectsDir   = os.path.join(os.path.dirname(__file__), 'mapObjects/native')
    externalMapObjectsDir = os.path.join(os.path.dirname(__file__), 'mapObjects/external')
    objCollection = ObjectsCollection([nativeMapObjectsDir, externalMapObjectsDir])
    print("Map objects found: " + str(objCollection.allObjectTypes()))

    view = HouseView()
    view.show()

    model = MapModelGeneral(MapObjectModelGeneral, objCollection)

    controller = HouseController(view=view, houseModel=model)

    exitcode = app.exec_()

    sys.exit(exitcode)

if __name__ == '__main__':
    main()
