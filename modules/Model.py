from enum import Enum

class HouseSquareType(Enum):
    Empty   = 0
    Corner  = 1
    Wall    = 2
    Door    = 3

class HouseSquareRotation(Enum):
    deg0    = 0
    deg90   = 1
    deg180  = 2
    deg270  = 3

class HouseSquareTerritory(Enum):
    Empty       = 0
    Kitchen     = 1
    Bedroom     = 2
    LivingRoom  = 3
    StoreRoom   = 4

class HouseMapSquareModel:
    def __init__(self, id):
        self.id = id
        #self.typesList = ['None,', 'Corner', 'Wall', 'Door', 'Window']
        #self.rotationsList = [0, 90, 180, 370]
        #self.territoriesList = ['None', 'Kitchen', 'Bedroom', 'LivingRoom', 'StoreRoom']

        #self.typeId         = 0
        #self.rotationId     = 0
        #self.territoryId    = 0
        
        #print(len(HouseSquareType))
        #print(list(HouseSquareType))
        #for val in list(HouseSquareType):
        #    print("    " + val.name + "->" + str(val.value))
        
        self.properties = dict()
        self.properties['type']      = HouseSquareType.Empty
        self.properties['rotation']  = HouseSquareRotation.deg0
        self.properties['territory'] = HouseSquareTerritory.Empty

    def getXY(self):
        y = int(self.id / 1000)
        x = self.id % 1000

        return [x, y]


class HouseMapModel:
    def __init__(self):
        """Model initializer."""
        self.width = 0
        self.height = 0
        self._squares = dict()

    def initMap(self, h, w):
        self.width = w
        self.height = h
        for row in range(h):
            for column in range(w):
                id = row*1000 + column
                self._squares[id] = HouseMapSquareModel(id)

    def getSquare(self, id):
        return self._squares[id]


    def getAllSquares(self):
        return self._squares

    def size(self):
        return [self.height, self.width]


