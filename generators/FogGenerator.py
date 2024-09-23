from modules.GeneratorPluginBase import *

from random import random

TypeGrass  = "Grass"

class FogGenerator(GeneratorPluginBase):
    def __init__(self, mapModel):
        super().__init__(mapModel)
        self.fogModel = 'Fog'


    def generate(self):
        print("Generating fog")
        interval = int(self.settings['intervalSquares'])

        for col in range(0, self.mapModel.width, interval):
            for row in range(0, self.mapModel.height, interval):
                self._placeFog(row,col)

        self.mapModel.updateEntireMap()

        print("Done")

    def clear_generated(self):
        print("Clear generated Fog")
        res = self.mapModel.removeAllMapObjects(FogGenerator)
        if (True == res):
            self.mapModel.updateEntireMap()
            print("Done")
        elif (False == res):
            print("Done (was empty)")
        else:
            self.mapModel.updateEntireMap()
            print("Done (smth wrong)")

    def _placeFog(self, row, col):
        obj = MapObjectModelGeneral()
        obj.init(col, row, model = self.fogModel, modelGenerator = FogGenerator)
        self.mapModel.addMapObject(obj)
