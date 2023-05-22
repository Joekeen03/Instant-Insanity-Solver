from DepthFirstSolver import DepthFirstSolver
from SeparationSolver import SeparationSolver
from DivisionSolver import DivisionSolver
import SmallestObstacleFinder as small

from MinimalObstacleFallDown import TopDownObstacleFinder
from SeparationFinder import FindObstacleReductive, FindMaxGroups
from PuzzleGenerator import GeneratePuzzle, TEST_GENERATORS, TEST_PUZZLES, PUZZLE_GENERATORS
from Puzzle import SubPuzzle
from Result import TYPES

def PrintResult(result, *, tab="  ", tabCount=0, solutionLimit=8, subResult=False, printSubResults=True):
    lineFormatter = "\t"*tabCount+"{}"
    def PrintLine(text, subCount=0):
        print(tab*(tabCount+subCount)+(text))
    PrintLine("Result:")
    PrintLine(f"Is Full Solution: {result.isFullSolution}", 1)
    PrintLine(f"Result type: {result.resultType.name}", 1)
    if result.extra != None:
        PrintLine("Extra Info:", 1)
        PrintLine(f"{result.extra}", 2)
    PrintLine(f"Puzzle: {result.puzzle.name}", 1)
    for puzzleSlice in result.puzzle:
        PrintLine(f"{puzzleSlice}", 2)
    if result.isFullSolution:
        PrintLine("Full Solutions:", 1)
        i = 0
        for solution in result.solutions:
            PrintLine(f"{solution}", 2)
            i += 1
            if i >= solutionLimit:
                break
    if result.resultType == TYPES.Parent and printSubResults:
        PrintLine("Sub-results:", 1)
        for subResult in result.subResults:
            PrintResult(subResult, tabCount=tabCount+2, subResult=True)

def SolvePuzzle(puzzle, solverProc):
    result = solverProc(puzzle)
    print("*"*30)
    PrintResult(result, printSubResults=True)
    return result

def FindObstacles(puzzle, finder):
    print(f"Checking for obstacles for puzzle {puzzle.name}:")
    obstacles = finder(puzzle)
    print(f"\tObstacles for puzzle {puzzle.name}:")
    if len(obstacles) == 0:
        print("\t\tNo obstacles found.")
    else:
        print(f"\t\t{len(obstacles)} obstacle(s) found.")
        for obstacle in obstacles:
            print(f"\t\t{obstacle}")
    return obstacles

def ProcessTests(processor):
    for puzzleID in TEST_GENERATORS:
        puzzle = GeneratePuzzle(puzzleID, source=TEST_GENERATORS)
        processor(puzzle)
    for puzzle in TEST_PUZZLES:
        processor(puzzle)

def ProcessAssignmentPuzzles(processor):
    for puzzleID in PUZZLE_GENERATORS:
        puzzle = GeneratePuzzle(puzzleID, source=PUZZLE_GENERATORS)
        processor(puzzle)

def main():
    solver = SeparationSolver
    solverProc = lambda puzzle: SolvePuzzle(puzzle, solver)
    minimalFile = open("minimalObstacles.txt", 'w')
    logFile = open("minimalLogger.log", 'w')
    saveObstacle = lambda puzzle: minimalFile.write(f"Puzzle:\n{puzzle}\nSmallest Obstacle:\n{small.FindSmallestObstacle(puzzle)}\n")
    #SolvePuzzle(TEST_PUZZLES[2], solver)
    #ProcessTests(small.FindSmallestObstacle)
    #ProcessAssignmentPuzzles(solverProc)
    
    #finder = lambda puzzle : TopDownObstacleFinder(puzzle, DepthFirstSolver)
    finder = lambda puzzle: [small.FindSmallestObstacle(puzzle)]
    finderProc = lambda puzzle: FindObstacles(puzzle, finder)
    #FindObstacles(TEST_PUZZLES[1], finder)
    #puzzle = GeneratePuzzle(1, PUZZLE_GENERATORS)
    #obstacle = FindObstacles(puzzle, finder)[0]
    ProcessAssignmentPuzzles(lambda puzzle: print(f"Puzzle:\n{puzzle}\nSmallest obstacle:\n{small.FindSmallestObstacle(puzzle, logFile)}\n\n", file=minimalFile, flush=True))
    
    #puzzle = GeneratePuzzle(6, source=PUZZLE_GENERATORS)
    small.FindSmallestObstacle(puzzle)
    #print("Testing permutations.")
    #for index in obstacle.mappingIndices:
        #print(f"Excluding index {index}")
        #result = solver(SubPuzzle(puzzle, list(range(index))+list(range(index+1, len(puzzle)))))
        #if result.isFullSolution:
            #print(result)
    #solverProc(obstacle)
    #ProcessTests(finderProc)
    #ProcessAssignmentPuzzles(finderProc)
    minimalFile.close()
    logFile.close()

main()
