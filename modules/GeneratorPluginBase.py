import os
import inspect

from modules.MapModelGeneral import *

class GeneratorPluginBase:
    def __init__(self, mapModel):
        self.mapModel = mapModel
        self.pluginSettings = {}
        self.schema = {}
        #childPluginClassName = self.__class__.__name__
        childPluginLocation = inspect.getfile(self.__class__);
        self.settingsFileName = os.path.splitext(childPluginLocation)[0] + '.json'
        self.loadPluginSettings2()

    def loadPluginSettings2(self):
        with open(self.settingsFileName, 'r') as f:
            #print("FIle content:" + f.read())
            self.pluginSettings = json.load(f)
            print(">SETTINGS: " + str(self.pluginSettings))
            self.schema = self.pluginSettings['schema']
            
            print(">SCHEMA: " + str(self.schema))

    #def loadPluginSettings(self):
    #    with open(self.settingsFileName, 'w') as f:
    #        json.dump(self.pluginSettings, f, indent=4)

    def generate(self, settings):
        raise NotImplementedError("Each plugin must implement the run method.")
