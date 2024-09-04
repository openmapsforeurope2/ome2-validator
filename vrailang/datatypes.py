'''
The `vrailang.datatypes` module contains datatypes that can be used as type annotations in featureclasses.

Implementation note:
Some of these types inherit from builtin types such as `int`, `float` or `str`.
The sole purpose of this inheritance is to provide some type hints when a featureclass is instantiated like a dataclass.
The datatypes within this module themselves are not instantiated.

Implementation note 2:
For the same reason, the `DataType` base class inherits from `MixinAttributeRules` from the `vrailang.rules` module
in order to provide type hints.
'''


from typing import Annotated
from qgis.core import QgsGeometry
from vrailang.rules import MixinAttributeRules

# TODO: Document implementation notes, such as having these types inherit from int, float, str, etc.
#                                                                          (but also e.g. MixinAttributeRules)
#       --> Rationale: it's just for the type hints, since we are not actually instantiating any of these types

__all__ = [
    'smallint', 'integer', 'bigint',
    'smallserial', 'serial', 'bigserial',

    'numeric', 'decimal',
    'uuid',
    'timestamp',

    'real', 'double_precision',

    'varchar', 'text',

    'multilinestringz',
]


class classproperty:
    def __init__(self, func):
        self.fget = func
    def __get__(self, instance, owner):
        return self.fget(owner)

VARIABLE_SIZE = -1


class DataType(MixinAttributeRules):
    """The base class for various datatypes."""

    @classproperty
    def size(cls):
        raise NotImplemented('Subclasses of DataType should have a field or classproperty `size`')
    
    def __class_getitem__(cls, *specifications):
        if not isinstance(specifications[0], tuple):
            specifications = (specifications,)
        return Annotated.__class_getitem__((cls,) + specifications)


class IntegralType(DataType, int):
    pass

class smallint(IntegralType):
    size = 2

class integer(IntegralType):
    size = 4

class bigint(IntegralType):
    size = 8

class bigint(IntegralType):
    size = 8

class smallserial(smallint):
    pass

class serial(integer):
    pass

class bigserial(bigint):
    pass


class numeric(DataType, float):
    size = VARIABLE_SIZE

decimal = numeric


class uuid(IntegralType):
    size = 16 # 128 bits



class FloatingPointType(DataType, float):
    pass

class real(FloatingPointType):
    size = 4

class double_precision(FloatingPointType):
    size = 8


class timestamp(FloatingPointType):
    size = 8


class CharacterType(DataType, str):
    pass

class varchar(CharacterType):
    size = VARIABLE_SIZE

class text(CharacterType):
    size = VARIABLE_SIZE



class GeometryType(DataType, QgsGeometry):
    size = VARIABLE_SIZE

class multilinestringz(GeometryType):
    pass