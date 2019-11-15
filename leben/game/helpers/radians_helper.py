import math


def get_periphery_radians(x, y, a, b, r):
    """
    base: (x, y)
    target: (a, b), r

    return None when base and target are in same pixel.
    """
    if x == a and b == y:
        return None, None
    R = math.sqrt((b - y)**2 + (a - x)**2)
    radians_delta = math.atan2(r, R)

    center_radians = math.atan2((b - y), (a - x))
    return (center_radians - radians_delta), (
        center_radians + radians_delta), R


def get_regulate_periphery_radians(x, y, a, b, r):
    l_radians, r_radians = get_periphery_radians(x, y, a, b, r)


def regulate_radians(radians):
    return radians % (2 * math.pi)


def regulate_radians_range(radians, left, right):
    left = regulate_radians(left)
    right = regulate_radians(right)
    radians = regulate_radians(radians)

    if left > right:
        if radians < right:
            radians += 2 * math.pi
        right += 2 * math.pi
    return radians, left, right


def regulate_radians_between(radians, left, right):
    radians, left, right = regulate_radians_range(radians, left, right)
    return radians < right and radians > left


def radians_between(radians, left, right):
    return radians < right and radians > left
