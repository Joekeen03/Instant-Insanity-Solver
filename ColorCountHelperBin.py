# Binary
def CreateColorCountsBin(nColors=N_SLICES, nSides=N_SIDES):
    assert nColors <= 32, "nColors cannot be more than 32"
    return [0]*nSides

def CopyColorsBin(sideColors):
    return list(sideColors)

def ComputeRotationBin(sideColors, currSlice, rotationIndex, nSides=N_SIDES):
    result = CopyColorsBin(sideColors)
    for sideIndex in range(nSides):
        actualIndex = (rotationIndex + sideIndex) % nSides
        color = 1 << currSlice[actualIndex]
        if (color & result[sideIndex]):
            return None
        result[sideIndex] = color
    return result

def ComputeRotationSetBin(colorsBase, slices, rotations, nSides=N_SIDES):
    #print(f"Rotation set. {colorsBase}, {slices}, {rotations}")
    result = CopyColorsBin(colorsBase)
    for i in range(len(slices)):
        result = ComputeRotationBin(result, slices[i], rotations[i], nSides)
        if result == None:
            return None
    return result
