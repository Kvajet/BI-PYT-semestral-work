from math import floor
from random import random


def random_int(mod: int = 10) -> int:
    return floor(random() * 10000) % mod
