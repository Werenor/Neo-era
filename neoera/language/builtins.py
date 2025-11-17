class Builtins:# neoera/language/builtins.py
import random


def random_int(a, b):
    return random.randint(int(a), int(b))


def random_float(a, b):
    return random.uniform(float(a), float(b))


def to_number(x):
    try:
        return float(x)
    except:
        return 0


def to_bool(x):
    if isinstance(x, str):
        return x != ""
    if isinstance(x, (int, float)):
        return x != 0
    return bool(x)


def contains(a, b):
    return a in b


BUILTINS = {
    "random": random_int,
    "random_float": random_float,
    "len": lambda x: len(x),
    "num": to_number,
    "bool": to_bool,
    "contains": contains,
}
