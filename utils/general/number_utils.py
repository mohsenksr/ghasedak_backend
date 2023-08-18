from math import floor


def truncate(number, digits=6):
    factor = 10 ** (-1 * digits)
    return floor(number * (10 ** 6)) / (10 ** 6)
