from DepthFirstSolver import DepthFirstSolver
from SeparationSolver import SeparationSolver
from Puzzle import SubPuzzle
from itertools import chain

def FindObstacleReductive(puzzle):
    result = DepthFirstSolver(puzzle)
    if result.isFullSolution:
        return None
    swapIndex = 0 # Index to place the next slice in the minimal obstacle. Aka the size of the minimal obstacle constructed so far
    furthestIndex = result.extra.furthestGone # Index of the next slice in the minimal obstacle
    order = list(range(len(puzzle)))
    # Use >= instead of >. In cases where the last slice to move isn't already in the position it'll end up at, > would work - the last slice would be swapped,
    # the swap index would end up == to the size of the obstacle (1 greater than the last element), and the furthest index would end up at the last element in
    # the obstacle - furthest<swap. However, in the case where the last slice IS in the position it'll be moved to, what would happen is that on the penultimate
    # swap, the furthest index is set to that final postion. As that final position is also where the last slice in the obstacle should be transferred, the while
    # loop will terminate prematurely - furthest==swap, which is not furthest>swap
    # I guess you could just detect that case, as it would allow you to skip creating and solving a subpuzzle.
    # Alright, using '>' for the while loop, and doing an equality comparison afterwards.
    while furthestIndex > swapIndex:
        # Build up the minimal obstacle at the start
        order[swapIndex], order[furthestIndex] = order[furthestIndex], order[swapIndex]
        subPuzzle = SubPuzzle(puzzle, order)
        # Determine the new indices
        furthestIndex = DepthFirstSolver(subPuzzle).extra.furthestGone
        swapIndex += 1

    # No need to create a new subpuzzle, as we know the furthestIndex slice is part of the minimal obstacle
    if furthestIndex == swapIndex:
        swapIndex += 1
    
    return SubPuzzle(puzzle, order[:swapIndex])



def FindMaxGroups(puzzle):
    obstacles = []
    subPuzzle = puzzle
    result = FindObstacleReductive(puzzle)
    while result != None:
        obstacles.append(result)
        subPuzzle = SubPuzzle(subPuzzle, [i for i in range(len(subPuzzle)) if i not in result.mappingIndices])
        result = FindObstacleReductive(subPuzzle)
    return obstacles

def SeparationFinder(puzzle):
    obstacles = []
    
