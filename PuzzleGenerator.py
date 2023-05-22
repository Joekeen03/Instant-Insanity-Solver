import math
from Puzzle import Puzzle

N_SLICES = 31
N_SIDES = 3
GENERIC_GENERATOR = lambda f : (lambda n : 1 + (math.floor(n*f) % N_SLICES))
PUZZLE_GENERATORS = {1 : GENERIC_GENERATOR(17*math.pi**6),
                     2 : GENERIC_GENERATOR(17*math.e**6),
                     3 : GENERIC_GENERATOR(17*math.e**8),
                     4 : GENERIC_GENERATOR(11*math.e**8),
                     5 : GENERIC_GENERATOR(101*math.e**2),
                     6 : GENERIC_GENERATOR(101*math.e**8),}

TEST_GENERATORS = {"test1": lambda n : 1 + (n-1 - ((n-1)%N_SIDES))//N_SIDES,}
TEST_PUZZLES = (Puzzle("test2", ((1, 2, 3), (1, 2, 3), (1, 2, 3))),
                Puzzle("test3", ((1, 1, 2), (2, 2, 1), (3, 4, 5), (3, 4, 5), (5, 4, 3))),
                Puzzle("test4", ((1, 1, 2), (2, 2, 1), (3, 4, 5), (3, 4, 5), (3, 4, 5))),)

def GenerateColors(generator, nSlices):
    # Generates the slices for a puzzle, given that puzzle's generator
    slices = []
    colorCounts = [0,]*nSlices
    n = 1
    # Generate all N_SLICES slices
    for sliceIndex in range(nSlices):
        currSlice = []
        sideIndex = 0
        # Generate the i'th slice
        while sideIndex < N_SIDES:
            # Get the next color
            colorID = generator(n)
            n += 1
            # If the next color hasn't occurred N_SIDES times, add it to the current slice
##            print(colorID)
            if colorCounts[colorID-1] < N_SIDES:
                currSlice.append(colorID)
                colorCounts[colorID-1] += 1
                sideIndex += 1
        slices.append(tuple(currSlice))
    return tuple(slices)

def ValidatePuzzle(puzzle, nSlices):
    assert len(puzzle) == nSlices
    colorCounts = [0,]*nSlices
    for singleSlice in puzzle:
        assert len(singleSlice) == N_SIDES
        for sideColor in singleSlice:
            assert (sideColor >= 1) and (sideColor <= nSlices)
            colorCounts[sideColor-1] += 1
            assert colorCounts[sideColor-1] <= N_SIDES
    for count in colorCounts:
        assert count == N_SIDES

def GeneratePuzzle(puzzleID, source=PUZZLE_GENERATORS, nSlices=N_SLICES):
    # Generates and returns a specified puzzle. If the puzzle is invalid, throws an AssertionError
    # If the puzzleID doesn't correspond to a defined puzzle, returns None.
    if puzzleID in source:
        puzzle = GenerateColors(source[puzzleID], nSlices)
##        print(puzzle)
        ValidatePuzzle(puzzle, nSlices)
        return Puzzle(puzzleID, puzzle)
    return None

def test():
    for puzzleID in PUZZLE_GENERATORS:
        print(GeneratePuzzle(puzzleID))

if __name__ == "__main__":
    test()
