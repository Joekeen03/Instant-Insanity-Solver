from ColorCountHelper import CreateColorCounts, ComputeRotationSet

class Solution(object):
    def __init__(self, rotations):
        assert type(rotations) in (list, tuple), "Rotations must be a list of indices."
        self.rotations = rotations

    def __str__(self):
        return "Solution: {}".format(self.rotations)

class SolutionGenerator(object):
    def __iter__(self):
        raise NotImplementedError("Solution Generator iterator hasn't been implemented!")
    
    def __str__(self):
        return "Solution Generator base class."

# A generator which takes a puzzle, and a list of solutions to subpuzzles of that puzzle, and returns all possible combinations of the sub-results' solutions
# Implemented as a generator because if you're dealing with N independent puzzles, you could easily have 3^(N-1) possible solutions
# Implemented as a class, so that I can easily check its type in Result
# FIXME Docs need to be fixed

class SolutionJoiner(SolutionGenerator):
    class SolutionChunk(object):
        def __init__(self, subResult):
            self.subResult = subResult

        def __iter__(self):
            raise NotImplementedError("__iter__ wasn't implemented for this!")

    class SolutionBase(SolutionChunk):
        def __init__(self, subResult):
            super().__init__(subResult)
            solutionSize = len(subResult.puzzle.parent)-1
            #print(solutionSize)
            self.base = (-1,)*solutionSize

        def __iter__(self):
            def Generator():
                for solution in self.subResult.solutions:
                    yield RemapSolution(solution.rotations, list(self.base), self.subResult.puzzle.mappingIndices[1:])
            return Generator()
    
    class SolutionFragment(SolutionChunk):
        def __init__(self, prefix, subResult):
            super().__init__(subResult)
            self.prefix = prefix
            self.nSides = len(self.subResult.puzzle[0])

        def __iter__(self):
            def Generator():
                for prefix in self.prefix:
                    for solution in self.subResult.solutions:
                        for i in range(self.nSides):
                            yield RemapSolution((0,)+solution.rotations, list(prefix), self.subResult.puzzle.mappingIndices, rotation=i)
            return Generator()
    
        
    def __init__(self, subResults):
        self.solution = self.SolutionBase(subResults[0])
        for res in subResults[1:]:
            self.solution = self.SolutionFragment(self.solution, res)

    def __iter__(self):
        return (Solution(rotations) for rotations in self.solution)

    def __str__(self):
        return "Solution Joiner object."

class SolutionValidator(SolutionGenerator):
    def __init__(self, subResults):
        self.solution = self.ValidationBase(subResults[0])
        for res in subResults[1:]:
            self.solution = self.ValidationFragment(self.solution, res)

    def __iter__(self):
        return (Solution(tuple(rotations)) for colorCount, rotations in self.solution)

    def __str__(self):
        return "Solution Validator object."

    class ValidationChunk(object):
        def __init__(self, subResult):
            self.subResult = subResult
            self.nSides = len(subResult.puzzle[0])

        def __iter__(self):
            raise NotImplementedError("__iter__ wasn't implemented for this!")

    class ValidationBase(ValidationChunk):
        def __init__(self, subResult):
            super().__init__(subResult)
            solutionSize = len(subResult.puzzle.parent)-1
            self.rotationBase = (-1,)*solutionSize
            self.colorBase = CreateColorCounts(nColors=len(subResult.puzzle.GetOrigin()), nSides=self.nSides)

        def __iter__(self):
            def BaseGenerator():
                for solution in self.subResult.solutions:
                    augmentedRotations = (0,)+solution.rotations
                    colorCounts = ComputeRotationSet(self.colorBase, self.subResult.puzzle, augmentedRotations, self.nSides)
                    if colorCounts == None:
                        raise ValueError("SolutionBase received an invalid solution! Solution: {solution.rotations}")
                    rotations = RemapSolution(solution.rotations, list(self.rotationBase), self.subResult.puzzle.mappingIndices[1:])
                    yield (colorCounts, rotations)
            return BaseGenerator()
    
    class ValidationFragment(ValidationChunk):
        def __init__(self, prefix, subResult):
            super().__init__(subResult)
            self.prefix = prefix

        def __iter__(self):
            def FragmentGenerator():
                for prefixColors, prefixRotations in self.prefix:
                    for solution in self.subResult.solutions:
                        augmentedRotations = (0,)+solution.rotations
                        for i in range(self.nSides):
                            #print(prefixColors)
                            colorCounts = ComputeRotationSet(prefixColors, self.subResult.puzzle, RotateRotations(augmentedRotations, i, self.nSides), self.nSides)
                            #print(colorCounts)
                            if colorCounts != None:
                                yield (colorCounts, RemapSolution(augmentedRotations, list(prefixRotations), self.subResult.puzzle.mappingIndices, rotation=i))
            return FragmentGenerator()

# Takes a list of slice rotations, and returns each rotation rotated 'delta' positions
def RotateRotations(rotations, delta, nSides=3):
    return [(i+delta)%nSides for i in rotations]

def RemapSolution(source, destination, mapping, rotation=0, nSides=3):
    for i, val in zip(mapping, source):
        destination[i-1] = (val+rotation)%nSides
    return destination

