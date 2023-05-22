from enum import Enum
from itertools import repeat, cycle
from Solutions import Solution, SolutionGenerator

# TODO Make this store nonsolutions in 'results', and solutions in 'solutions' member variables?
#  Also have some way to distinguish solutions with multiple solutions
# Ideal: "furthestGone", "solution", "solutions", "subsolutions" (?)

TYPES = Enum("Result Types", ("Parent", "Leaf"))

class Result(object):
    def __init__(self, puzzle, isFullSolution, resultType=TYPES.Leaf, subResults=None, solutions=None, extra=None):
        self.puzzle = puzzle
        self.isFullSolution = isFullSolution
        assert isFullSolution == (solutions != None), "No full solution passed to a complete result." if isFullSolution else "Full solution passed to a partial result."
        
        self.solutions = solutions
        if isFullSolution:
            assert isinstance(solutions, (list, tuple, Solution, SolutionGenerator)),\
                   f"Solutions should be a list or tuple of Solution objects, a single Solution object, or a Solution generator. Received: {type(solutions)}"
            if type(self.solutions) == Solution:
                self.solutions = (self.solutions,)

        self.resultType = resultType
        self.subResults = subResults
        if resultType is TYPES.Leaf:
            assert subResults == None, "Terminal-result solver shouldn't have sub-results."
        elif resultType is TYPES.Parent:
            assert subResults != None, "Nested-result solver should have at least one sub-result."
            assert type(subResults) in (list, tuple, Result), "Sub-results should be a list/tuple of Result objects, or a single Result object."
            if type(subResults) == Result:
                subResults = (subResults,)
            self.subResults = subResults
        else:
            raise ValueError("resultType was not a valid result type from TYPES. Received: {}".format(resultType))
        self.extra = extra

    def __str__(self):
        returnValue = f"Result:\n\tIs Full Solution: {self.isFullSolution}\n\tResult type: {self.resultType.name}"
        if self.extra != None:
            returnValue += f"\n\tExtra Info:\n\t\t{self.extra}"
        returnValue += "\n\tPuzzle:"
        for puzzleSlice in self.puzzle:
            returnValue += f"\n\t\t{puzzleSlice}"
        if self.isFullSolution:
            returnValue += "\n\tFull Solutions:"
            for solution in self.solutions:
                returnValue += f"\n\t\t{solution}"
        if self.resultType == TYPES.Parent:
            returnValue += "\n\tSub-results:"
            for result in self.subResults:
                returnValue += f"\n\t\t{result}"
        return returnValue
