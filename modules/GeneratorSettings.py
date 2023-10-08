from modules.GeometryPrimitives import *
from modules.SerializableSettings import *

# TODO: can we get variable type from current object?
#    in this case we no longer need all the hardcoded class parsers
class LandObject():
    def __init__(self, size=AreaSize(0.0,0.0), probability=0.0):
        self.size = AreaSize(size.w, size.h)
        self.probability = probability
        
    def loadFromDict(self, settings):
        for k, v in settings.items():
            if k == 'size':
                a = AreaSize(0.0, 0.0)
                a.loadFromDict(v)
                setattr(self, k, a)
            else:
                setattr(self, k, v)
                
class ObjectVariant():
    def __init__(self):
        self.name = ""
        self.size = AreaSize(0.0, 0.0)
        self.probability = 0.0
        
    def loadFromDict(self, settings):
        for k, v in settings.items():
            if k == 'size':
                a = AreaSize(0.0, 0.0)
                a.loadFromDict(v)
                setattr(self, k, a)
            else:
                setattr(self, k, v)
        
                
class LandObjectWithVariants(LandObject):
    def __init__(self, probability=0.0):
        self.variants = list()
        # one empty variant to add new object in the properties editor
        self.variants.append(ObjectVariant())
        self.probability = probability
        
    def loadFromDict(self, settings):
        for k, v in settings.items():
            if k == 'variants':
                self.variants = list()
                for item in v:
                    a = ObjectVariant()
                    a.loadFromDict(item)
                    self.variants.append(a)
            elif k == 'size':
                a = AreaSize(0.0, 0.0)
                a.loadFromDict(v)
                setattr(self, k, a)
            else:
                setattr(self, k, v)
        
       

class LandLotSettings():
    def __init__(self):
        self.size = AreaSize(15, 20)
        self.roadWidth = 2

        self.house = LandObjectWithVariants(probability = 0.8);
        self.shed  = LandObject(AreaSize(2,2), probability = 0.5);

        self.treeProbability = 0.2

    def loadFromDict(self, settings):
        for k, v in settings.items():
            if k == 'size':
                a = AreaSize(0, 0)
                a.loadFromDict(v)
                setattr(self, k, a)
            elif k == 'house':
                a = LandObjectWithVariants()
                a.loadFromDict(v)
                setattr(self, k, a)
            elif k == 'shed':
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

