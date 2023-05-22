# TODO Add nSides, nColors, nSlices parameter
#   Maybe create a PuzzleGenerator class?
class Puzzle(object):
    def __init__(self, puzzleName, puzzleArray):
        self.puzzleArray = puzzleArray
        self.name = str(puzzleName)

    def GetOrigin(self):
        return self
        
    def __str__(self):
        return f"Puzzle object: {self.name}\n\tPuzzle:{self.puzzleArray}"

    def __getitem__(self, indices):
        try:
            return self.puzzleArray[indices]
        except TypeError as e:
            raise TypeError(f"Puzzle Error: {e}")

    def __len__(self):
        return len(self.puzzleArray)

class SubPuzzle(Puzzle):
    def __init__(self, parent, mappingIndices):
        indexList = tuple(mappingIndices) # In case mappingIndices is a generator. Also, so we have an immutable copy of the indices
        super().__init__(parent.name+f":subset{indexList}", [parent.puzzleArray[i] for i in indexList])
        self.parent = parent
        self.mappingIndices = indexList
        self.origin = parent.GetOrigin()
        

    def GetOrigin(self):
        return self.origin

    def __str__(self):
        return f"Subpuzzle object: {self.name}\n\tPuzzle:{self.puzzleArray}"

