from modules.GeometryPrimitives import *
from modules.SerializableSettings import *

class LandObject():
    def __init__(self, size=AreaSize(0,0), probability=0):
        self.size = AreaSize(size.w, size.h)
        self.probability = probability
        
    def loadFromDict(self, settings):
        for k, v in settings.items():
            if k == 'size':
                a = AreaSize(0, 0)
                a.loadFromDict(v)
                setattr(self, k, a)
            else:
                setattr(self, k, v)

class LandLotSettings():
    def __init__(self):
        self.size = AreaSize(15, 20)
        self.roadWidth = 2

        self.house = LandObject(AreaSize(7,7), probability = 0.8);
        self.shed  = LandObject(AreaSize(2,2), probability = 0.5);

        self.treeProbability = 0.2

    def loadFromDict(self, settings):
        for k, v in settings.items():
            if k == 'size':
                a = AreaSize(0, 0)
                a.loadFromDict(v)
                setattr(self, k, a)
            elif (k == 'house') or (k == 'shed'):
                a = LandObject()
                a.loadFromDict(v)
                setattr(self, k, a)
            else:
                setattr(self, k, v)

class GeneratorSettings(SerializableSettings):
    def __init__(self):
        super().__init__("settings/terrainGenerator.json")

        self.rows = 2
        self.columns = 5

        self.landLotSettings = LandLotSettings()

        self.forestKeepOut = 3
        self.roadWidth = 2

    def loadFromDict(self, settings):
        for k, v in settings.items():
            if k == 'landLotSettings':
                z = LandLotSettings()
                z.loadFromDict(v)
                setattr(self, k, z)
            else:
                setattr(self, k, v)

