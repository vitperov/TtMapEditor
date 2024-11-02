from enum import Enum
from PyQt5.QtCore import *

from modules.MapModelGeneral import *
from modules.ObjectsCollection import *
from modules.GeneratorPluginsLoader import *
from modules.ApplicationSettings.ApplicationSettingsModel import ApplicationSettingsModel

class Model:
    def __init__(self):
        settings = ApplicationSettingsModel()
        nativeMapObjectsDir   = os.path.join(os.getcwd(), 'mapObjects')
        externalMapObjectsDir = settings.getAdditionalMapObjectsDir()
        self.objCollection = ObjectsCollection([nativeMapObjectsDir, externalMapObjectsDir])
        #print("Map objects found: " + str(self.objCollection.allObjectTypes()))

        self.map = MapModelGeneral(MapObjectModelGeneral, self.objCollection)
        
        pluginsDir = 'generators'
        self.generators = GeneratorPluginsLoader(self.map)
        self.generators.loadPluginsFrom(pluginsDir)
        #print("Generator plugins found: " + str(self.generators.generators))
   

