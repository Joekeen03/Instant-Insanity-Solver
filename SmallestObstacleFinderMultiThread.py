import SeparationFinder as SF
import SeparationSolver as SS
import ColorCountHelper as CCH
import Puzzle as puzz

import time, math

OUTPUT_LIMIT = 5
TIME_PER_SET = 0.002/5.17 # Estimated time per subset, in seconds. Computed based on average time for a size-7 subset
N_THREADS = 4

# Takes a puzzle, and the max size subset to search for, and returns the smallest
# obstacle found in the puzzle, or an empty subset if no obstacle was found
def DepthFirstFinder(puzzle, maxLength, startDepth=0, logFile=None):
    tStart = time.perf_counter()
    limit = maxLength-1-1
    puzzleLength = len(puzzle)
    nSides = len(puzzle[0])
    rotations = list(range(nSides))
    smallestObstacle = []
    print(f"Searching for obstacles starting at size {maxLength-1}", file=logFile, flush=True)

    def GeneratePartialSolutions(prevSolutions, sliceID):
        currSlice = puzzle[sliceID]
        partialSolutions = []
        for rot in rotations:
            for prevSolution in prevSolutions:
                partialSolution = CCH.ComputeRotation(prevSolution, currSlice, rot)
                if partialSolution != None:
                    partialSolutions.append(partialSolution)
        return partialSolutions

    def DFThreadWrapper(startSolutions, depth, startIndex, threadID):
        indices = list(range(limit+1))
        indices[depth] = startIndex
        setSize = limit-startDepth
        tSubStart = time.perf_counter()

        def UpdateSmallest(depth):
            subPuzzle = puzz.SubPuzzle(puzzle, indices[:depth+1])
            temp = SF.FindObstacleReductive(subPuzzle)
            smallestObstacle = list(map(lambda i: subPuzzle.mappingIndices[i], temp.mappingIndices))
            PrintThread(smallestObstacle) # Switch to mutex...turns out the GIL is kind of a problem
            limit = min(len(smallestObstacle)-1-1, limit)
            PrintThread(f"Minimal obstacle size reduced to {limit+1}, while processing subset of size {depth+1}")

        def ConditionalOutput(depth, sliceID):
            PrintThread(f"Searching @ {depth}/{limit} (depth/limit), slice ID {sliceID}")
            return f"Finished searching @ {depth}/{limit} (depth/limit), slice ID {sliceID}. Time taken: {{:.4f}} seconds."

        def PrintThread(text):
            print("[Thread:f{threadID}]{text)", file=logFile, flush=True)
        
        def DFRecursiveFast(prevSolutions, depth, startIndex):
            nonlocal limit, smallestObstacle
            # Try every possible subset of size (limit-depth), starting at startIndex
            j = startIndex
            while (j < (puzzleLength-limit+depth)) and (limit >= depth):
                indices[depth] = j
                # Compute all rotations, so we can readily see if this is solvable
                currSolutions = GeneratePartialSolutions(prevSolutions, j)
                if len(currSolutions) > 0: # This particular subset has a solution
                    if depth < limit:
                        DFRecursiveFast(currSolutions, depth+1, j+1)
                else: # This particular subset has no solution; begin searching for a smaller obstacle
                    subPuzzle = puzz.SubPuzzle(puzzle, indices[:depth+1])
                    temp = SF.FindObstacleReductive(subPuzzle)
                    smallestObstacle = list(map(lambda i: subPuzzle.mappingIndices[i], temp.mappingIndices))
                    PrintThread(smallestObstacle)
                    limit = min(len(smallestObstacle)-1-1, limit)
                    PrintThread(f"Minimal obstacle size reduced to {limit+1}, while processing subset of size {depth+1}")
                    return
                j += 1

        def DFRecursive(prevSolutions, depth, startIndex):
            nonlocal limit, smallestObstacle
            # Try every possible subset of size (limit-depth), starting at startIndex
            j = startIndex
            while j < (puzzleLength-limit+depth):
                tStart = time.perf_counter()
                f = ConditionalOutput(depth, j)
                indices[depth] = j
                # Compute all rotations, so we can readily see if this is solvable
                currSolutions = GeneratePartialSolutions(prevSolutions, j)
                if len(currSolutions) > 0: # This particular subset has a solution
                    if depth < limit:
                        if (limit-depth) > OUTPUT_LIMIT:
                            DFRecursive(currSolutions, depth+1, j+1)
                        else:
                            DFRecursiveFast(currSolutions, depth+1, j+1)
                else: # This particular subset has no solution; begin searching for a smaller obstacle
                    subPuzzle = puzz.SubPuzzle(puzzle, indices[:depth+1])
                    temp = SF.FindObstacleReductive(subPuzzle)
                    smallestObstacle = list(map(lambda i: subPuzzle.mappingIndices[i], temp.mappingIndices))
                    PrintThread(smallestObstacle)
                    limit = min(len(smallestObstacle)-1-1, limit)
                    PrintThread(f"Minimal obstacle size reduced to {limit+1}, while processing subset of size {depth+1}")
                    return
                j += 1
                tEnd = time.perf_counter()
                print(f.format(tEnd-tStart), file=logFile, flush=True)
        
        f = ConditionalOutput(startDepth, startIndex)
        subSetSize = math.factorial(puzzleLength-startIndex-1)/(math.factorial((puzzleLength-startIndex-1) - setSize)*math.factorial(setSize))
        print(f"Estimated time: {TIME_PER_SET*subSetSize}", file=logFile, flush=True)
        DFRecursive(startSolutions, depth, startIndex)
        tSubEnd = time.perf_counter()
        print(f.format(tSubEnd-tSubStart), file=logFile, flush=True)

    baseColors = CCH.CreateColorCounts(nColors=len(puzzle.GetOrigin()), nSides=nSides)
    startColors = []
    if startDepth > 0:
        startColors = [CCH.ComputeRotation(baseColors, puzzle[0], 0)]
        for i in range(1, startDepth):
            startColors = GeneratePartialSolutions(startColors, i)
    
    j = startDepth
    threads = []
    tLoopStart = time.perf_counter()
    while (j < (puzzleLength-limit+startDepth)) and (limit > startDepth):
        sideColors = None
        if startDepth == 0:
            sideColors = [CCH.ComputeRotation(baseColors, puzzle[j], 0)]
        else:
            sideColors = GeneratePartialSolutions(startColors, j)
        DFThreadWrapper(sideColors, startDepth+1, j+1)
        j += 1
    tEnd = time.perf_counter()
    print(f"Depth-first search for minimal obstacles took {tEnd-tStart:.4f} seconds.", file=logFile, flush=True)
    return puzz.SubPuzzle(puzzle, smallestObstacle)

# Returns a tuple of the elements for the range [0, length), minus the excluded elements
def ExcludeIndices(length, exclude):
    exclude = sorted(exclude)
    base = list(range(length))
    for i in reversed(exclude):
        base.pop(i)
    return tuple(base)

# Finds all slices that are in all minimal obstacles, and also identifies the smallest minimal obstacle it's encountered
def FindRequiredSmaller(puzzle, obstacle):
    requiredSlices = []
    puzzleLength = len(puzzle)
    smallestObstacle = obstacle
    for index in obstacle.mappingIndices:
        subPuzzle = puzz.SubPuzzle(puzzle, ExcludeIndices(puzzleLength, (index,)))
        result = SF.SeparationSolver(subPuzzle)
        if result.isFullSolution:
            requiredSlices.append(index)
        else:
            tempObstacle = SF.FindObstacleReductive(subPuzzle)
            if len(tempObstacle) < len(smallestObstacle):
                smallestObstacle = tempObstacle
    return requiredSlices, smallestObstacle

def FindSmallestObstacle(puzzle, logFile=None):
    print(f"Processing puzzle:\n{puzzle}", file=logFile, flush=True)
    if logFile != None:
        print(f"Processing puzzle:\n{puzzle}")
    result = SS.SeparationSolver(puzzle)
    if result.isFullSolution:
        return None

    smallestObstacle = None
    for subResult in result.subResults:
        if not subResult.isFullSolution:
            subPuzzle = subResult.puzzle
            print(f"Searching independent subpuzzle:\n{subPuzzle}", file=logFile, flush=True)
            firstObst = SF.FindObstacleReductive(subPuzzle)
            print(f"Found a minimal obstacle:\n{firstObst}", file=logFile, flush=True)
            required, obst = FindRequiredSmaller(subPuzzle, firstObst)
            print(f"Identified required slices: {required}", file=logFile, flush=True)
            if obst != firstObst:
                print(f"Found smaller minimal obstacle:\n{obst}", file=logFile, flush=True)
            if smallestObstacle == None:
                smallestObstacle = obst
            optimizedSubPuzzle = puzz.SubPuzzle(subPuzzle, tuple(required)+ExcludeIndices(len(subPuzzle), required)) # Move required slices to the front of the puzzle
            print(f"Optimized subPuzzle:\n{optimizedSubPuzzle}", file=logFile, flush=True)
            currObst = DepthFirstFinder(optimizedSubPuzzle, min(len(obst), len(smallestObstacle)), len(required), logFile)
            if len(currObst) != 0:
                smallestObstacle = currObst
    print(f"Smallest obstacle:\n{smallestObstacle}\n\n----------", file=logFile, flush=True)
    return smallestObstacle
