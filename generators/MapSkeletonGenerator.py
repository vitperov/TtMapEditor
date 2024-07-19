from modules.GeneratorPluginBase import *

from random import random

TypeGrass  = "Grass"

class MapSkeletonGenerator(GeneratorPluginBase):
    def __init__(self, mapModel):
        super().__init__(mapModel)
        self.fogModel = 'Fog'


    def generate(self):
        print("Generating empty map")
        forestAroundMap = int(self.settings['forestAroundMap'])
        roadWidth       = int(self.settings['roadWidth'])
        leftExit        = bool(self.settings['leftExit'])
        rightExit       = bool(self.settings['rightExit'])
        landLotWidth    = int(self.settings['landLotWidth'])
        landLotHeight   = int(self.settings['landLotHeight'])
        landLotsRows    = int(self.settings['landLotsRows'])
        landLotsColumns = int(self.settings['landLotsColumns'])

        print("Done")

