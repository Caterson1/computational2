from random import randrange


def randomizer(x: tuple | float):
    if isinstance(x, tuple):
        return randrange(x[0], x[1], 1)
    return x
