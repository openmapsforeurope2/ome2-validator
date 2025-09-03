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
import textwrap
from typing import Annotated, Any, Callable, ClassVar, Generic, Optional, Protocol, Tuple, Type, TypeGuard, TypeVar, Union, cast, get_args, get_origin
from typing_extensions import Self

from vrailang._fastvarname import FastVarname
from vrailang.dataconstraints import DataTypeAnnotation, length
import vrailang.dataconstraints
from vrailang.datatypes import DataType, GeometryType, varchar
import vrailang.datatypes
from vrailang.errors import VraiSpecificationError
from vrailang.rules import MixinAttributeRules, MixinFeatureclassRules
import vrailang.specs

__all__ = [
    'feature',
    'is_featureclass'
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
_DataType = TypeVar('_DataType', bound=DataType)
@dataclass
class FeatureclassAttribute(Generic[_DataType], MixinAttributeRules[_DataType]):
    """The type used for describing a featureclass's fields.
    Instances of this class are added to a featureclass's class as class variables.
    """

    name: str
    '''Name of the field'''
    
    featureclass: Type['feature']
    '''To which featureclass this field belongs'''

    datatype: Type[_DataType]
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

    def __add__(cls, other) -> type['feature']:
        """Merges this featureclass with another.

        See `merged_with` for limitations.

        Example:
            transport_links = (road_link + railyway_link).with_alias('transport_links')

        Returns:
            type[feature]: The union of the two featureclasses.
        """

        # Support (+)-operator
        featureclass = cls
        if is_featureclass(featureclass):
            return featureclass.merged_with(other)
        raise VraiSpecificationError(f'cls {cls} is not a subtype of feature')

    def __new__(mcls, name: str, bases: Tuple[type], namespace: dict[str, Any], **kwargs: Any):

        # If this is the Feature class itself being created, no custom logic is required;
        # Likewise, if the class has been generated, the generating function can request to skip custom logic:
        if name == 'feature' or namespace.get('__skip_metaclass_logic__'):
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        # Otherwise, fetch the annotations and start building the class based on the annotations:
        annotations: dict[str, Union[type, str]] = namespace.get('__annotations__', {})
        
        featureclass_attrs: dict[str, FeatureclassAttribute] = OrderedDict()

        PATCH_IN_LATER: type[feature] = None # type: ignore # Featureclass is patched in later once created

        primary_key: FeatureclassAttribute | None = None
        geom_attr: FeatureclassAttribute[GeometryType] | None = None
        for field_name, annotation in annotations.items():
            origin = get_origin(annotation)

            if origin is None:
                field_type = annotation
                field_constraints = ()
            elif origin is Annotated:
                field_type, field_constraints = get_args(annotation)    
            else:
                raise AssertionError('Should not happen')
            
            if not vrailang.is_datatype(field_type):
                raise VraiSpecificationError(f'Attribute {field_name} in featureclass {name} has unsupported datatype: {field_type}')
            
            if not vrailang.are_dataconstraints(field_constraints):
                raise VraiSpecificationError(f'Constraints for {field_name} in featureclass {name} are not supported: {field_constraints}')

            namespace[field_name] = featureclass_attrs[field_name] = FeatureclassAttribute(
                field_name, PATCH_IN_LATER, field_type, field_constraints
            )

            if vrailang.dataconstraints.primary_key in field_constraints:
                if primary_key is None:
                    primary_key = namespace[field_name]
                else:
                    raise VraiSpecificationError(f'Attribute {field_name} in featureclass {name} is marked as primary key, but conflicts with primary key {primary_key.name}')
            
            if geom_attr is None and issubclass(field_type, GeometryType):
                geom_attr = namespace[field_name]

        if geom_attr is None:
            raise VraiSpecificationError(f'Featureclass {name} is missing a geometry attribute')

        namespace['PRIMARY_KEY'] = primary_key
        namespace['GEOMETRY_ATTRIBUTE'] = geom_attr
        namespace['ATTRIBUTES'] = featureclass_attrs
        
        # Set the theme
        if vrailang.specs.CURRENT_SPEC_STATE.current_theme is not None:
            namespace['THEME'] = vrailang.specs.CURRENT_SPEC_STATE.current_theme
        else:
            raise VraiSpecificationError('A featureclass must be defined between begin_theme() and end_theme()')
        
        # Create the class
        namespace['TABLE_NAME'] = name
        namespace.setdefault('ALIAS', None)
        new_featureclass = cast(type['feature'], 
            super().__new__(mcls, name, bases, namespace, **kwargs)
        )

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

    TABLE_NAME: ClassVar[str]
    '''The table name of the featureclass. Default: the name of the class.'''

    ALIAS: ClassVar[str | None]
    '''Optional alias for the featureclass that will be used for setting the layer name.'''

    ATTRIBUTES: ClassVar[dict[str, FeatureclassAttribute[DataType]]]
    '''All declared attributes of the featureclass.'''

    PRIMARY_KEY: ClassVar[FeatureclassAttribute[DataType] | None]
    '''The featureclass's attribute that functions as its primary key.'''

    GEOMETRY_ATTRIBUTE: ClassVar[FeatureclassAttribute[GeometryType]]
    '''The featureclass's geometry attribute.'''

    THEME: ClassVar[vrailang.specs.ValidationTheme]
    '''The `ValidationTheme` this featureclass belongs to.'''

    FILTER_QUERY: ClassVar[str | None] = None
    '''Optional filter query on the featureclass.'''

    @classmethod
    def with_alias(cls, new_alias: str) -> type[Self]:
        """Creates a renamed copy of the featureclass.

        Args:
            new_alias (str): the alias to use for the renamed copy.

        Returns:
            type[Self]: The featureclass with a new alias.
        """
        class RenamedFeatureclass(cls):
            ALIAS = new_alias
            __skip_metaclass_logic__ = True
        
        # Copy the name of the original featureclass
        RenamedFeatureclass.__name__ = cls.__name__
        return RenamedFeatureclass # type: ignore

    @classmethod
    def filtered(cls, query: str, alias: str | None = ...) -> type[Self]: # type: ignore
        """Creates a subselection of a featureclass.

        Args:
            query (str): The subselection filter query.
            alias (str): An alias for the subselection. Optional. 
                         If no alias is given, an attempt will be made to derive the alias 
                         based on the variable it is assigned to.
                         
                         Note that if `filtered` is used in an expression to create a validation check,
                         the subselection's alias could be set to be the name of the validation check,
                         like if the statement is of the form `Check_xxx = fc.filtered(...).MustAdhereToSomeRule()`.
                         If this behavior is undesirable, the alias argument must be set explicitly, e.g.,
                         `Check_xxx = fc.filtered(..., alias=None).MustAdhereToSomeRule()`.

        Returns:
            type[Self]: The sub-featureclass specified by the given query.
        """
        
        if cls.FILTER_QUERY is not None:
            query = f'({cls.FILTER_QUERY}) AND ({query})'

        # Attempt to derive alias automatically
        if alias is ...:
            fv = FastVarname(depth=2)
            if fv.varname is not None:
                alias = fv.varname
                
        class FilteredFeatureclass(cls):
            ALIAS = alias
            FILTER_QUERY = query
            __skip_metaclass_logic__ = True
        
        # Copy the name of the original featureclass
        FilteredFeatureclass.__name__ = cls.__name__
        return FilteredFeatureclass # type: ignore

    @classmethod
    def merged_with(cls, other: type['feature']) -> type['feature']:
        """Merges this featureclass with another featureclass.
        
        Limitations:
        The other featureclass must be of the same geometry type.
        Both featureclasses must have a primary key of type uuid.
        The names of the primary key and geometry columns in this
        featureclass must be the same as in the other featureclass.

        Args:
            other (feature): The other featureclass to merge.
        
        Returns:
            feature: The merged featureclass.
        """
        return merge([cls, other])
    
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
            
            if type(self) is not type(other):
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


def _flatten(featureclasses: list[type[feature]]) -> list[type[feature]]:
    res: list[type[feature]] = []

    for fc in featureclasses:
        nested_classes = getattr(fc, '__featureclasses__', None)
        if nested_classes: 
            res.extend(_flatten(nested_classes))
        else:
            res.append(fc)
    
    return res

def merge(featureclasses: list[type[feature]]) -> type[feature]:
    """Merges a collection of featureclasses into a combined featureclass.
        
    Limitations:
    The geometry type must be the same for all featureclasses.
    The geometry column must have the same name in all featureclasses.
    The primary key column must have the same name in all featureclasses.
    The primary key must be of type uuid.
    
    Args:
        featureclasses (list[type[feature]]): The featureclasses to merge.

    Returns:
        type[feature]: The union of the given featureclasses.
    """

    NEW_SRC_COLUMN = '__original_featureclass'

    # Collect all featureclasses into a flat list
    featureclasses = _flatten(featureclasses)
    if len(featureclasses) == 0:
        raise VraiSpecificationError('cannot merge 0 featureclasses')
    
    # Check geometry constraint: all featureclasses must be of the same type
    geom_attr_names: dict[str, list[str]] = {} # store for each name the featureclass names
    geom_attr_types: dict[type[GeometryType], list[str]] = {} # store for each type the featureclass names
    # + Check PK constraint: should be uuid and have same name
    pk_attr_names: dict[str, list[str]] = {} # store for each name the featureclass names
    pk_attr_missing: set[str] = set()
    pk_attr_wrong_types: dict[type[DataType], list[str]] = {} # store for each type the featureclass names
    for fc in featureclasses:
        fc_name = fc.ALIAS or fc.TABLE_NAME
        geom_attr_names.setdefault(fc.GEOMETRY_ATTRIBUTE.name, []).append(fc_name)
        geom_attr_types.setdefault(fc.GEOMETRY_ATTRIBUTE.datatype, []).append(fc_name)

        if fc.PRIMARY_KEY:
            pk_attr_names.setdefault(fc.PRIMARY_KEY.name, []).append(fc_name)
            if fc.PRIMARY_KEY.datatype is not vrailang.datatypes.uuid:
                pk_attr_wrong_types.setdefault(fc.PRIMARY_KEY.datatype, []).append(fc_name)
        else:
            pk_attr_missing.add(fc_name)
            
    
    if len(geom_attr_names) != 1:
        raise VraiSpecificationError(f'To be merged featureclasses should have geometry attributes with the same name, but found:\n\t{',\n\t'.join(
            f'{name} ({', '.join(geom_attr_names[name])})' for name in geom_attr_names
        )}')
    if len(geom_attr_types) != 1:
        raise VraiSpecificationError(f'To be merged featureclasses should have geometry attributes of the same type, but found:\n\t{',\n\t'.join(
            f'{geom_type.__name__} ({', '.join(geom_attr_types[geom_type])})' for geom_type in geom_attr_types
        )}')
    if len(pk_attr_missing) > 0:
        raise VraiSpecificationError(
            'To be merged featureclasses should have primary keys defined. Missing primary key:\n\t'
            + '\n\t'.join(pk_attr_missing)
        )
    if len(pk_attr_names) != 1:
        raise VraiSpecificationError(f'To be merged featureclasses should have primary key attributes with the same name, but found:\n\t{',\n\t'.join(
            f'{name} ({', '.join(pk_attr_names[name])})' for name in pk_attr_names
        )}')
    if len(pk_attr_wrong_types) > 0:
        raise VraiSpecificationError(f'To be merged featureclasses should have primary key attributes of type uuid. but found:\n\t{',\n\t'.join(
            f'{pk_type.__name__} ({', '.join(pk_attr_wrong_types[pk_type])})' for pk_type in pk_attr_wrong_types
        )}')

    # Determine common attributes (based on name)
    common_attribute_keys = sorted(set.intersection(*(
        set(fc.ATTRIBUTES)
        for fc in featureclasses
    )))
    
    if not common_attribute_keys:
        raise VraiSpecificationError('To be merged featureclasses should have at least have 1 common attribute')

    # Create union query
    sql = ' UNION ALL\n'.join(
        textwrap.dedent(f"""\
            (SELECT '{fc.THEME.schema}.{fc.TABLE_NAME}' {NEW_SRC_COLUMN},
                   {',\n                   '.join(f'"{column}"' for column in common_attribute_keys)}
             FROM {fc.THEME.schema}.{fc.TABLE_NAME}
             {f'WHERE {fc.FILTER_QUERY}' if fc.FILTER_QUERY else ''}
            )""")
        for fc in featureclasses
    )
    # Surround query with parentheses
    sql = f'({sql})'

    # Create merged featureclass
    class MergedFeatureClass(feature):
            __skip_metaclass_logic__ = True
            __featureclasses__ = featureclasses

            TABLE_NAME = sql
            ALIAS = '_'.join(fc.ALIAS or fc.TABLE_NAME for fc in featureclasses)

            ATTRIBUTES = {}
            PRIMARY_KEY = None
    
    # Copy common attributes into the merged feature class
    first_fc = featureclasses[0]
    MergedFeatureClass.ATTRIBUTES = {
        name: FeatureclassAttribute(
            name,
            MergedFeatureClass,
            first_fc.ATTRIBUTES[name].datatype,
            first_fc.ATTRIBUTES[name].constraints
        )
        for name in common_attribute_keys
    }

    # Set primary key
    primary_key = cast(FeatureclassAttribute, first_fc.PRIMARY_KEY)
    MergedFeatureClass.PRIMARY_KEY = FeatureclassAttribute(
        primary_key.name,
        featureclass=MergedFeatureClass,
        datatype=primary_key.datatype,
        constraints=primary_key.constraints
    )

    # Set the theme
    if vrailang.specs.CURRENT_SPEC_STATE.current_theme is not None:
        MergedFeatureClass.THEME = vrailang.specs.CURRENT_SPEC_STATE.current_theme
    else:
        raise VraiSpecificationError('A merged featureclass must be defined between begin_theme() and end_theme()')

    # Add __original_featureclass attribute
    MergedFeatureClass.ATTRIBUTES[NEW_SRC_COLUMN] = FeatureclassAttribute(
        NEW_SRC_COLUMN,
        MergedFeatureClass,
        varchar,
        (length(255),)
    )

    return MergedFeatureClass


def is_featureclass(cls: object) -> TypeGuard[type[feature]]:
    """Checks if a given type is a featureclass type.

    Example usage:
        ```
        # ...

        class RoadLine(feature):
            id: uuid[notnull]
            geom: multilinestringz[srid(3035)]
            name: varchar[length(255)]

        # ...

        res = is_featureclass(RoadLine) # returns True
        ```

    Args:
        cls (object): the type to check

    Returns:
        bool: True if and only if `cls` is a featureclass.
    """
    return issubclass(type(cls), FeatureMetaclass)
