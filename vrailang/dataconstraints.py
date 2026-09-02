'''
The `vrailang.dataconstraints` module contains constraints 
that can be applied to datatypes of the `vrailang.datatypes` module.
'''

from abc import ABC
from dataclasses import dataclass
from typing import TypeGuard

__all__ = [
    'is_dataconstraint', 'are_dataconstraints',

    'precision', 'scale',
    'length',
    'notnull',
    'primary_key',
    'srid'
]

class DataTypeAnnotation:
    pass

@dataclass
class SingleArgumentConstraint(ABC, DataTypeAnnotation):
    value: int

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

class precision(SingleArgumentConstraint):
    pass

class scale(SingleArgumentConstraint):
    pass

class length(SingleArgumentConstraint):
    pass

@dataclass
class boolean_flag(DataTypeAnnotation):
    name: str
    
    def __repr__(self):
        return self.name

notnull = boolean_flag('notnull')
primary_key = boolean_flag('primary_key')

@dataclass
class srid(DataTypeAnnotation):
    id: int


def is_dataconstraint(obj: object) -> TypeGuard[DataTypeAnnotation]:
    """Checks if a given object is an instance of DataTypeAnnotation.

    Args:
        obj (object): the object to check

    Returns:
        bool: True if and only if `obj` is a DataTypeAnnotation type.
    """
    return isinstance(obj, DataTypeAnnotation)


def are_dataconstraints(objects: object) -> TypeGuard[tuple[DataTypeAnnotation]]:
    """Checks if a given tuple objects are all an instance of DataTypeAnnotation.

    Args:
        objects (object): the objects to check

    Returns:
        bool: True if and only if `obj` is a tuple of dataconstraints.
    """
    return isinstance(objects, tuple) and all(
        is_dataconstraint(obj) for obj in objects
    )
