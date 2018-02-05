from enum import IntEnum

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Lang(IntEnum):
    Rus = 0
    Eng = 1
    Unknown = 2
