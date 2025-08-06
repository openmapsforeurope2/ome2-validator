'''
The `vrailang._protocols` module contains protocols and type aliases
for type hints purposes.
'''

from qgis.core import QgsVectorLayer
from typing import TYPE_CHECKING, Callable, ClassVar, Generic, Optional, Protocol, Self, Type, TypeVar

if TYPE_CHECKING:
    from vrailang.dataconstraints import DataTypeAnnotation
    from vrailang.datatypes import DataType, GeometryType
    from vrailang.featureclasses import feature, FeatureclassAttribute
    import vrailang.specs



_C = TypeVar("_C", bound='DataTypeAnnotation')
_DataType = TypeVar('_DataType', bound='DataType')
class FeatureclassAttributeProtocol(Generic[_DataType], Protocol):
    name: str
    featureclass: Type['feature']
    datatype: Type[_DataType]

    def get_constraint(self: Self, constraint_type: Type[_C]) -> Optional[_C]: ...



class FeatureclassProtocol(Protocol):
    ATTRIBUTES: ClassVar[dict[str, 'FeatureclassAttribute[DataType]']]
    PRIMARY_KEY: ClassVar['FeatureclassAttribute[DataType] | None']
    GEOMETRY_ATTRIBUTE: ClassVar['FeatureclassAttribute[GeometryType]']
    THEME: ClassVar['vrailang.specs.ValidationTheme']

    TABLE_NAME: ClassVar[str]
    ALIAS: ClassVar[str | None]
    FILTER_QUERY: ClassVar[str | None]
    

ArgLoader = Callable[[type['feature']], QgsVectorLayer] | Callable[[object], object]
