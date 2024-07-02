import importlib
import os
import pkgutil
from modules.GeneratorPluginBase import *

class GeneratorPluginsLoader:
    def __init__(self):
        self.generators = {}

    def loadPluginsFrom(self, directory):
        for _, name, is_pkg in pkgutil.iter_modules([directory]):
            if not is_pkg:
                module = importlib.import_module(f'generators.{name}')
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, PluginBase) and obj is not PluginBase:
                        self.generators[name] = obj()

    def printLoaded(self):
        for name, plugin in self.generators.items():
            print(f" {name}:")
