from modules.MapModelGeneral import *

class GeneratorPluginBase:
    def __init__(self, mapModel):
        self.mapModel = mapModel

    def generate(self, settings):
        raise NotImplementedError("Each plugin must implement the run method.")
