from Puzzle import SubPuzzle
from collections import namedtuple
from bitarray import bitarray

puzzleMask = namedtuple("puzzleMask", "puzzle, mask")

UPDATE_INTERVAL_MAX = 500
UPDATE_INTERVAL_MIN = 100
UPDATE_INTERVAL_COUNT = 10

def TopDownObstacleFinder(puzzle, solver):
    puzzleSize = len(puzzle)
    startMask = bitarray("0"*puzzleSize)
    oneMask = startMask|startMask
    oneMask[-1] = 1
    reverseMasks = tuple([oneMask<<i for i in range(puzzleSize)])
    masks = tuple([~rMask for rMask in reverseMasks])

    def GenerateSortedSubmasks(baseSets):
        #print(baseSets)
        subMasks = []
        if len(baseSets) > 0:
            subMasks = [None]*len(baseSets)*len(baseSets[0].puzzle)
        
        i = 0
        for baseSet in baseSets:
            baseMask = baseSet.mask
            for m in masks:
                subMask = baseMask & m
                if subMask != baseMask:
                    subMasks[i] = subMask
                    i += 1
        subMasks.sort()
        #print(len(subMasks))
        
        i = 0
        # Filter out duplicates
        for j in range(1, len(subMasks)):
            if subMasks[i] != subMasks[j]:
                i += 1
                subMasks[i] = subMasks[j]
        return subMasks[:i+1]

    def GenerateSubsets(baseSets):
        submasks = GenerateSortedSubmasks(baseSets)
        subsets = [puzzleMask(SubPuzzle(puzzle, (j for j in range(puzzleSize) if ((submask & reverseMasks[j]) != startMask))), submask)\
                   for submask in submasks]
        return subsets

    n = puzzleSize
    obstacles = []
    previousSubsets = []
    potentialObstacles = []
    currentSubsets = [puzzleMask(puzzle, ~startMask)]
    while (n >= 2) and (len(currentSubsets) > 0):
        print(f"\tChecking {len(currentSubsets)} subset(s) of size {n}. {len(obstacles)} found so far.")
        # Identify all unsolvable subsets
        i = 0
        interval = min(UPDATE_INTERVAL_MAX, max(UPDATE_INTERVAL_MIN, len(currentSubsets)//UPDATE_INTERVAL_COUNT))
        for subset in currentSubsets:
            #print(subset.puzzle)
            if not solver(subset.puzzle).isFullSolution:
                #print(subset.puzzle)
                potentialObstacles.append(subset)
            i+=1
            if (i % interval) == 0:
                print(f"\t\tChecked {i} subsets of {len(currentSubsets)} subsets")

        # Remove all larger subsets which contain one of the obstacles
        for previousSubset in previousSubsets:
            for subset in potentialObstacles:
                if (subset.mask & previousSubset.mask)==subset.mask:
                    break
            else:
                obstacles.append(previousSubset)

        # Compute all new, unique subsets
        previousSubsets = potentialObstacles
        potentialObstacles = []
        currentSubsets = GenerateSubsets(previousSubsets)
        n -= 1
    # Exited out b/c n=2
    if len(currentSubsets) > 0:
        obstacles.extend(previousSubsets)
    
    return tuple([ob.puzzle for ob in obstacles])
