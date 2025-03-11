
class SelectionRange:
    def __init__(self, startCol, startRow, endCol, endRow, zLevel):
        self.startCol = startCol
        self.startRow = startRow
        self.endCol = endCol
        self.endRow = endRow
        self.zLevel = zLevel
    
    @classmethod
    def fromStartPointAndSize(cls, startPoint, size, zLevel):
        return cls(startPoint.x, startPoint.y, startPoint.x + size.w - 1, startPoint.y + size.h - 1, zLevel)
