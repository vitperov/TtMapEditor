from enum import Enum
try:
    from PyQt5.QtCore import *
except:
    from PyQt4.QtCore import *

from modules.MapModelGeneral import *
from modules.ObjectsCollection import *
from modules.GeneratorPluginsLoader import *

class Model:
    def __init__(self):
        nativeMapObjectsDir   = os.path.join(os.getcwd(), 'mapObjects/native')
        externalMapObjectsDir = os.path.join(os.getcwd(), 'mapObjects/external')
        self.objCollection = ObjectsCollection([nativeMapObjectsDir, externalMapObjectsDir])
        #print("Map objects found: " + str(self.objCollection.allObjectTypes()))

        self.map = MapModelGeneral(MapObjectModelGeneral, self.objCollection)
        
        pluginsDir = 'generators'
        self.generators = GeneratorPluginsLoader(self.map)
        self.generators.loadPluginsFrom(pluginsDir)
        #print("Generator plugins found: " + str(self.generators.generators))
   

