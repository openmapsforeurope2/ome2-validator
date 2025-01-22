'''
The `vrailang.featureclasses` module contains the `feature` base class 
that can be used to describe a featureclass.

Example usage:

    ```
    from vrailang import *

    begin_theme('DEMO')

    class RoadLine(feature):
        id: uuid[notnull]
        geom: multilinestringz[srid(3035)]
        name: varchar[length(255)]

    end_theme()
    ```
'''

from abc import ABCMeta
from collections import OrderedDict
from dataclasses import dataclass
from typing import Annotated, Any, Callable, ClassVar, Optional, Protocol, Tuple, Type, TypeGuard, TypeVar, Union, get_args, get_origin
from typing_extensions import Self

from vrailang.dataconstraints import DataTypeAnnotation
from vrailang.datatypes import DataType
from vrailang.errors import VraiSpecificationError
from vrailang.rules import MixinAttributeRules, MixinFeatureclassRules
import vrailang.specs

__all__ = [
    'feature',
    'isfeatureclass'
]

# https://github.com/microsoft/pyright/blob/597ccabd07bdb977e535380675092aca839ef692/specs/dataclass_transforms.md
_T = TypeVar("_T")
def __dataclass_transform__(
    *,
    eq_default: bool = True,
    order_default: bool = False,
    kw_only_default: bool = False,
    field_descriptors: Tuple[Union[type, Callable[..., Any]], ...] = (()),
) -> Callable[[_T], _T]:
    # If used within a stub file, the following implementation can be
    # replaced with "...".
    return lambda a: a


_C = TypeVar("_C", bound=DataTypeAnnotation)
@dataclass
class FeatureclassAttribute(MixinAttributeRules):
    """The type used for describing a featureclass's fields.
    Instances of this class are added to a featureclass's class as class variables.
    """

    name: str
    '''Name of the field'''
    
    featureclass: Type['feature']
    '''To which featureclass this field belongs'''

    datatype: DataType
    '''The field's datatype'''
    
    constraints: Tuple[DataTypeAnnotation]
    '''Constraints on the datatype'''

    def get_constraint(self: Self, constraint_type: Type[_C]) -> Optional[_C]:
        """Returns constraint.

        Args:
            constraint_type (Type[_C]): The type of constraint to find.

        Returns:
            Optional[_C]: The queried constraint for this attribute, if any.
        """
        return next(filter(lambda c: isinstance(c, constraint_type), self.constraints), None) # type: ignore
        
    


@__dataclass_transform__(kw_only_default=True)
class FeatureMetaclass(ABCMeta):


    def __new__(mcls, name: str, bases: Tuple[type], namespace: dict[str, Any], **kwargs: Any):

        # If this is the Feature class itself being created, no custom logic is required:
        if name == 'feature':
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        # Otherwise, fetch the annotations and start building the class based on the annotations:
        annotations: dict[str, Union[type, str]] = namespace.get('__annotations__', {})
        
        featureclass_attrs: dict[str, FeatureclassAttribute] = OrderedDict()

        PATCH_IN_LATER = None

        for field_name, annotation in annotations.items():
            origin = get_origin(annotation)

            if origin is None:
                field_type = annotation
                field_constraints = ()
            elif origin is Annotated:
                field_type, field_constraints = get_args(annotation)    
            else:
                raise AssertionError('Should not happen')
            
            namespace[field_name] = featureclass_attrs[field_name] = FeatureclassAttribute(
                field_name, PATCH_IN_LATER, field_type, field_constraints
            )
        
        namespace['ATTRIBUTES'] = featureclass_attrs
        
        # Set the theme
        if vrailang.specs.CURRENT_SPEC_STATE.current_theme is not None:
            namespace['THEME'] = vrailang.specs.CURRENT_SPEC_STATE.current_theme
        else:
            raise VraiSpecificationError('A featureclass must be defined between begin_theme() and end_theme()')
        
        # Create the class
        new_featureclass = super().__new__(mcls, name, bases, namespace, **kwargs)

        # Patch the reference to the new class into the featureclass attributes
        for attr in featureclass_attrs.values():
            attr.featureclass = new_featureclass
        
        # Register ourselves to the theme
        vrailang.specs.CURRENT_SPEC_STATE.current_theme.feature_classes[name] = new_featureclass
        
        return new_featureclass



class FeatureMetaclassWithProtocolSupport(type(Protocol), FeatureMetaclass): # type: ignore
    """
    This metaclass combines `FeatureMetaclass` with `Protocol`'s metaclass,
    such that `feature` can inherit subclasses of `Protocol`.
    If `feature` were to use `FeatureMetaclass` instead when inheriting a `Protocol`,
    the following error is raised:
    
        `metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases`
    """
    pass

class feature(MixinFeatureclassRules, metaclass=FeatureMetaclassWithProtocolSupport):
    """The base class for featureclasses."""

    ATTRIBUTES: ClassVar[dict[str, FeatureclassAttribute]]
    '''All declared attributes of the featureclass.'''

    THEME: ClassVar[vrailang.specs.ValidationTheme]
    '''The `ValidationTheme` this featureclass belongs to.'''

    def __init__(self, **data):
        for k in self.ATTRIBUTES.keys():
            v = data.get(k, None)
            setattr(self, k, v)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        data = ', '.join(
            f'{k}={repr(getattr(self, k))}'
            for k in self.ATTRIBUTES.keys()
        )
        return f'{name}({data})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, feature):
            
            if type(self) != type(other):
                return False
            
            if self.__dict__ == other.__dict__:
                return True
            
            for k in type(self).ATTRIBUTES:
                v1 = getattr(self, k)
                v2 = getattr(other, k)
                if v1 != v2:
                    return False
            else:
                return True

        return False


def isfeatureclass(cls: object) -> TypeGuard[type[feature]]:
    """Checks if a given type is a featureclass type.

    Example usage:
        ```
        # ...

        class RoadLine(feature):
            id: uuid[notnull]
            geom: multilinestringz[srid(3035)]
            name: varchar[length(255)]

        # ...

        res = isfeatureclass(RoadLine) # returns True
        ```

    Args:
        cls (object): the type to check

    Returns:
        bool: True if and only if `cls` is a featureclass.
    """
    return issubclass(type(cls), FeatureMetaclass)
