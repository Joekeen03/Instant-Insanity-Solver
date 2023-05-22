from PuzzleGenerator import N_SIDES, N_SLICES

def CreateColorCounts(nColors=N_SLICES, nSides=N_SIDES):
    return [[False,]*nColors,]*nSides

def CopyColors(sideColors):
    copy = []
    for side in sideColors:
        copy.append(list(side))
    return tuple(copy)

def __ComputeRotationInPlace(sideColors, currSlice, rotationIndex, nSides=N_SIDES):
    #print("Compute Rotation")
    for sideIndex, sideColor in enumerate(currSlice):
        actualIndex = (rotationIndex + sideIndex) % nSides
        if not sideColors[actualIndex][sideColor-1]:
            sideColors[actualIndex][sideColor-1] = True
        else: # Second occurence of a color on a side, rotation is invalid
            return False
    return True

def ComputeRotation(sideColors, currSlice, rotationIndex, nSides=N_SIDES):
    result = CopyColors(sideColors)
    if not __ComputeRotationInPlace(result, currSlice, rotationIndex, nSides):
        return None
    return result

def ComputeRotationSet(colorsBase, slices, rotations, nSides=N_SIDES):
    #print(f"Rotation set. {colorsBase}, {slices}, {rotations}")
    result = CopyColors(colorsBase)
    for i in range(len(slices)):
        if not __ComputeRotationInPlace(result, slices[i], rotations[i], nSides):
            return None
    return result
