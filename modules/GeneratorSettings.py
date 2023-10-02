from modules.GeometryPrimitives import *

class ZoneSettings():
    def __init__(self):
        self.size = AreaSize(15, 20)
        self.roadWidth = 2

        # TODO: randomly choose house
        self.houseSize = AreaSize(7, 7)
        self.houseProbability = 0.9

        self.shedSize = AreaSize(2, 2)
        self.shedProbability = 0.5

        self.treeProbability = 0.2

    def loadFromDict(self, settings):
        for k, v in settings.items():
            if (k == 'houseSize') or \
               (k == 'shedSize'):
                a = AreaSize(0, 0)
                a.loadFromDict(v)
                setattr(self, k, a)
            else:
                setattr(self, k, v)

class GeneratorSettings:
    def __init__(self):
        self.zoneSettings = ZoneSettings()
        self.rows = 2
        self.columns = 5

        self.zoneSettings = ZoneSettings()

        self.forestKeepOut = 3
        self.roadWidth = 2

    def loadFromDict(self, settings):
        for k, v in settings.items():
            if k == 'zoneSettings':
                z = ZoneSettings()
                z.loadFromDict(v)
                setattr(self, k, z)
            else:
                setattr(self, k, v)

