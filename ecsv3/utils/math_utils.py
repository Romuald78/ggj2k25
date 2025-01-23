import math


def distance(x0, y0, x1, y1):
    dx = x0 - x1
    dy = y0 - y1
    return math.sqrt(dx*dx + dy*dy)

