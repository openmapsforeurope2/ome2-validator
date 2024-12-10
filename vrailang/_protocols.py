'''
The `vrailang._protocols` module contains protocols
for type hints purposes.
'''

from typing import TYPE_CHECKING, ClassVar, Optional, Protocol, Self, Type, TypeVar, Union

if TYPE_CHECKING:
    from vrailang.dataconstraints import DataTypeAnnotation
    from vrailang.datatypes import DataType
    from vrailang.featureclasses import feature, FeatureclassAttribute
    import vrailang.specs



_C = TypeVar("_C", bound='DataTypeAnnotation')
class FeatureclassAttributeProtocol(Protocol):
    name: str
    featureclass: Type['feature']
    datatype: 'DataType'

    def get_constraint(self: Self, constraint_type: Type[_C]) -> Optional[_C]: ...



class FeatureclassProtocol(Protocol):
    ATTRIBUTES: ClassVar[dict[str, 'FeatureclassAttribute']]
    THEME: ClassVar[Union['vrailang.specs.ValidationTheme', None]]
    