from modules.MapModelGeneral import *

class RespawnGenerator():
    def __init__(self, model, settings, objModelName):
        self.model = model
        self.settings = settings
        self.respawnModel = objModelName


    # Find squares surrounded by trees. There can be 8 squares of forest maximum,
    # and don't forget to have at least one square to get out.
    def generateHiddenRespawns(self, minForest=6, maxForest=7):
        def isForest(row, col):
            if row < 0:
                return False
            if row >= self.model.height:
                return False
            if col < 0:
                return False
            if col >= self.model.width:
                return False

            square = self.model.getSquare(col, row)
            sqType = square.getProperty('type')
            
            return sqType == SquareType.Forest
            

        def isHiddenSquare(row, col):
            if isForest(row, col):
                return False; # respawn can't be in the square with a tree
                
            forestSquares = 0;
            for r in [row-1, row, row+1]:
                for c in [col-1, col, col+1]:
                    if isForest(r, c):
                        forestSquares += 1
                        
            return (forestSquares >= minForest) and (forestSquares <= maxForest)
            
        #FIXME: we can reduce available area excuding forest border
        for col in range(self.model.width):
            for row in range(self.model.height):
                if isHiddenSquare(row, col):
                    self.placeRespawn(row,col)
                    
                    
    def placeRespawn(self, row, col):
        obj = MapObjectModel(col, row, self.respawnModel)
        self.model.addMapObject(obj)

