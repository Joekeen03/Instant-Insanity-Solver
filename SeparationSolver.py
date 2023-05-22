from DepthFirstSolver import DepthFirstSolver
from Result import TYPES, Result
from Solutions import Solution, SolutionJoiner
from Puzzle import SubPuzzle

def ShareColors(puzzle, baseIndexSet, testIndex):
    for baseIndex in baseIndexSet:
        for color in puzzle[baseIndex]:
            if color in puzzle[testIndex]:
                return True
    return False

# Takes a puzzle, and returns the slices split into independent groups.
# Specifically, returns both the groups of slices, and the original index of each slice.
def SeparatePuzzles(puzzle):
    puzzleIndices = [i for i in range(len(puzzle))]
    groups = []
    while len(puzzleIndices) > 0:
        subPuzzleIndices = [puzzleIndices.pop(0)]
        added = True
        while added:
            added = False
            for i in range(len(puzzleIndices)-1, -1, -1):
                if ShareColors(puzzle, subPuzzleIndices, puzzleIndices[i]):
                    subPuzzleIndices.append(puzzleIndices.pop(i))
                    added = True
        subPuzzleIndices.sort()
        groupPuzzle = SubPuzzle(puzzle, subPuzzleIndices)
        groups.append(groupPuzzle)
    return groups

def SeparationSolver(puzzle, subSolver=DepthFirstSolver):
    subPuzzles = SeparatePuzzles(puzzle)
    subResults = []
    for subPuzzle in subPuzzles:
        subResults.append(subSolver(subPuzzle))
    for subResult in subResults:
        if not subResult.isFullSolution:
            # How do I handle the subpuzzles, since they need to be remapped to the main puzzle?
            # Do I just not worry about it for partial solutions?
            return Result(puzzle, isFullSolution=False, resultType=TYPES.Parent,
                          subResults=subResults)
    return Result(puzzle, isFullSolution=True, resultType=TYPES.Parent,
                  subResults=subResults, solutions=SolutionJoiner(subResults))
