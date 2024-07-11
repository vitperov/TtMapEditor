import importlib
import os
import pkgutil
import warnings

from modules.GeneratorPluginBase import *

class GeneratorPluginsLoader:
    def __init__(self, mapModel):
        self.generators = {}
        self.mapModel = mapModel

    def loadPluginsFrom(self, directory):
        modulePath = directory.replace(os.sep, '.')
        while modulePath.startswith('.'):
            modulePath = modulePath[1:]

        for _, name, is_pkg in pkgutil.iter_modules([directory]):
            fullModuleName = f'{modulePath}.{name}'

            if not is_pkg:
                print("Importing: " + fullModuleName)
                module = importlib.import_module(fullModuleName)
                found_plugin = False
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, GeneratorPluginBase) and obj is not GeneratorPluginBase:
                        self.generators[name] = obj(self.mapModel)
                        found_plugin = True
                if not found_plugin:
                    warnings.warn(f"Module '{fullModuleName}' does not contain any class derived from GeneratorPluginBase")
            else :
                print("Loading packages is not implemented: " + fullModuleName)

    def printLoaded(self):
        for name, plugin in self.generators.items():
            print(f" {name}:")
