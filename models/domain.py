from enum import Enum

class BaseValueDomain(Enum):

    @classmethod
    def to_list(cls):
        return list(map(lambda x: x.value, cls))
