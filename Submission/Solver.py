import SmallestObstacleFinder as small

from PuzzleGenerator import GeneratePuzzle, TEST_GENERATORS, TEST_PUZZLES, PUZZLE_GENERATORS

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
    minimalFile = open("minimalObstacles.txt", 'w')
    logFile = open("minimalLogger.log", 'w')
    saveObstacle = lambda puzzle: minimalFile.write(f"Puzzle:\n{puzzle}\nSmallest Obstacle:\n{small.FindSmallestObstacle(puzzle)}\n")
    finder = lambda puzzle: [small.FindSmallestObstacle(puzzle)]
    finderProc = lambda puzzle: FindObstacles(puzzle, finder)
    ProcessAssignmentPuzzles(lambda puzzle: print(f"Puzzle:\n{puzzle}\nSmallest obstacle:\n{small.FindSmallestObstacle(puzzle, logFile)}\n\n", file=minimalFile, flush=True))
    
    minimalFile.close()
    logFile.close()
