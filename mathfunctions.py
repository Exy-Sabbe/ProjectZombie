from os import path

def GetSquaredDistance(position1, position2):
    return (position1[0] - position2[0])**2 + (position1[1] - position2[1])**2

def IsPositionInRange(own_pos, other_pos, max_range):
    return GetSquaredDistance(own_pos, other_pos) <= max_range**2

def GetHealthColor(health, maxhealth):
    return (255 - (health / maxhealth * 255), health / maxhealth * 255, 0)

def GetImagePath(imageName):
    return path.join(path.dirname(path.realpath(__file__)), path.join("images", imageName))