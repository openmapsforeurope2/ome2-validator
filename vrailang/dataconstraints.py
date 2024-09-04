'''
The `vrailang.dataconstraints` module contains constraints 
that can be applied to datatypes of the `vrailang.datatypes` module.
'''

from dataclasses import dataclass

__all__ = [
    'precision', 'scale',
    'length',
    'notnull',
    'srid'
]

class DataTypeAnnotation:
    pass

@dataclass
class precision(DataTypeAnnotation):
    value: int

@dataclass
class scale(DataTypeAnnotation):
    value: int


@dataclass
class length(DataTypeAnnotation):
    value: int

@dataclass
class boolean_flag(DataTypeAnnotation):
    name: str
    
    def __repr__(self):
        return self.name

notnull = boolean_flag('notnull')

@dataclass
class srid(DataTypeAnnotation):
    id: int
