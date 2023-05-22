def FindObstacle(puzzle, solver):
    def FindObstacleRecursive(subset, startIndex, remaining):
        for i in range(startIndex, len(puzzle)-remaining):
            currentSet = subset+(puzzle[i],)
            if (remaining > 0):
                FindObstacleRecursive(currentSet, i+1, remaining-1)
            else:
                result = solver(currentSet)
                if not result.isSolution:
                    return subset
    for i in range(len(puzzle)):
        print("Checking all subsets of size {}".format(i))
        obstacle = FindObstacleRecursive((), 0, i)
        
