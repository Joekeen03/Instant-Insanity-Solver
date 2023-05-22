import PuzzleGenerator
from Result import TYPES, Result
from Solutions import Solution
from ColorCountHelper import *

def DepthFirstSolver(puzzle):
    def DepthFirstSubSolver(sideColors, sliceID):
        maxDepth = sliceID
        assert (sideColors == None) == (sliceID == 0) # Something broke if this fails
        if (sliceID >= len(puzzle)): # Reached the end, we've found a solution
            return ()
        else:
            # Try all three rotations for the given side
            for rotationIndex in range(PuzzleGenerator.N_SIDES):
                # Current orientation
                nextColors = ComputeRotation(sideColors, puzzle[sliceID], rotationIndex)
                if nextColors != None: # Orientation is valid
                    #print("Recursion...")
                    nextResult = DepthFirstSubSolver(nextColors, sliceID+1)
                    if (type(nextResult) == int): # Furthest possible for this branch
                        maxDepth = max(nextResult, maxDepth)
                    else:
                        # Found a valid solution
                        return (rotationIndex,)+nextResult
        # Couldn't find a valid solution for the rotations so far.
        return maxDepth
    # Start of the puzzle
    sideColors = ComputeRotation(CreateColorCounts(nColors = len(puzzle.GetOrigin()), nSides=len(puzzle[0])), puzzle[0], 0)
    result = DepthFirstSubSolver(sideColors, sliceID=1)
    if type(result) != int:
        return Result(puzzle, True, solutions=Solution(result))
    else:
        return Result(puzzle, False, extra=DepthFirstInfo(furthestGone=result))

class DepthFirstInfo(object):
    def __init__(self, *, furthestGone):
        self.furthestGone = furthestGone

    def __str__(self):
        return "Furthest gone: {}".format(self.furthestGone)
