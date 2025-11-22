import random

BUILTINS = {
    "random": lambda a, b: random.randint(int(a), int(b)),
    "random_float": lambda a, b: random.uniform(float(a), float(b)),
    "len": lambda x: len(x),
    "num": lambda x: float(x),
    "bool": lambda x: bool(x),
    "contains": lambda a, b: a in b,
}
