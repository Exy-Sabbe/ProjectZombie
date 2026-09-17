def GetSquaredDistance(position1, position2):
    return (position1[0] - position2[0])**2 + (position1[1] - position2[1])**2

def IsPositionInRange(own_pos, other_pos, max_range):
    return GetSquaredDistance(own_pos, other_pos) <= max_range**2