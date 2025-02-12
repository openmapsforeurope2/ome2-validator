'''
The `vrailang._protocols` module contains protocols and type aliases
for type hints purposes.
'''

from qgis.core import QgsVectorLayer
from typing import TYPE_CHECKING, Callable, ClassVar, Optional, Protocol, Self, Type, TypeVar

if TYPE_CHECKING:
    from vrailang.dataconstraints import DataTypeAnnotation
    from vrailang.datatypes import DataType
    from vrailang.featureclasses import feature, FeatureclassAttribute
    import vrailang.specs



_C = TypeVar("_C", bound='DataTypeAnnotation')
class FeatureclassAttributeProtocol(Protocol):
    name: str
    featureclass: Type['feature']
    datatype: Type['DataType']

    def get_constraint(self: Self, constraint_type: Type[_C]) -> Optional[_C]: ...



class FeatureclassProtocol(Protocol):
    ATTRIBUTES: ClassVar[dict[str, 'FeatureclassAttribute']]
    THEME: ClassVar['vrailang.specs.ValidationTheme']
    

ArgLoader = Callable[[type['feature']], QgsVectorLayer] | Callable[[object], object]
