from Result import Result, TYPES
from Solutions import Solution, SolutionValidator
from Puzzle import SubPuzzle
from ColorCountHelper import *
from PuzzleGenerator import N_SIDES

# TODO Set up DivisionSolver to use the SeparationSolver for puzzle halves
def DivisionSolver(puzzle):
    puzzleLength = len(puzzle)
    if puzzleLength == 1:
        # Return list of all distinct solutions
        # Each element in the list is a list of rotations for each slice
        return Result(puzzle, isFullSolution=True, solutions=Solution(()))
    else:
        middleIndex = puzzleLength//2
        subResults = (DivisionSolver(SubPuzzle(puzzle, range(middleIndex))),
                      DivisionSolver(SubPuzzle(puzzle, range(middleIndex, puzzleLength))))
        if subResults[0].isFullSolution and subResults[1].isFullSolution:
            validator = SolutionValidator(subResults)
            for s in validator:
                # Basically, if the validator returns at least one solution, we know we have a valid full solution
                return Result(puzzle, isFullSolution=True, resultType=TYPES.Parent, subResults=subResults, solutions=validator)
        # No solution found
        return Result(puzzle, isFullSolution=False, resultType=TYPES.Parent, subResults=subResults)
