from modules.GeometryPrimitives import *
from modules.SerializableSettings import *

class LandObject(DictLoadableObject):
    def __init__(self, size=AreaSize(0.0,0.0), probability=0.0):
        self.size = AreaSize(size.w, size.h)
        self.probability = probability

class ObjectVariant(DictLoadableObject):
    def __init__(self):
        self.name = ""
        self.size = AreaSize()
        self.probability = 0.0

class LandObjectWithVariants(LandObject):
    def __init__(self, probability=0.0):
        self.variants = list()
        # we must provide at least one empyt value to be able
        #   to determine it's type later
        self.variants.append(ObjectVariant())
        self.probability = probability


class LandLotSettings(LandObject):
    def __init__(self):
        self.size = AreaSize(15, 20)
        self.roadWidth = 2

        self.house = LandObjectWithVariants(probability = 0.8);
        self.shed  = LandObject(AreaSize(2,2), probability = 0.5);

        self.treeProbability = 0.2


class GeneratorSettings(SerializableSettings):
    def __init__(self):
        super().__init__("settings/terrainGenerator.json")

        self.rows = 2
        self.columns = 5

        self.landLotSettings = LandLotSettings()

        self.forestKeepOut = 3
        self.roadWidth = 2

