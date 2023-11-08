from modules.Terrain.TerrainMapModel import *

class FogGenerator():
    def __init__(self, model, settings, objModelName):
        self.model = model
        self.settings = settings
        self.fogModel = objModelName


    def generate(self):
        interval = self.settings.fogInterval
        
        for col in range(0, self.model.width, interval):
            for row in range(0, self.model.height, interval):
                self.placeFog(row,col)
                    
                    
    def placeFog(self, row, col):
        obj = MapObjectModel(col, row, self.fogModel)
        self.model.addMapObject(obj)

