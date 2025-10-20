'''
The `vrailang.rules` module contains methods for creating `ValidationRule` objects.
These methods reside in `MixinAttributeRules` for rules pertaining to a featureclass's attributes
and in `MixinFeatureclassRules` for rules pertaining to a featureclass itself.
'''

from dataclasses import dataclass, field
from typing import Any, Generic, Type, TYPE_CHECKING, TypeVar, Union, cast
from typing_extensions import Self
from validators.abstract_validator import AbstractValidator
import validators
from vrailang._fastvarname import FastVarname
from vrailang._protocols import ArgLoader, FeatureclassProtocol, FeatureclassAttributeProtocol
from vrailang.errors import VraiSpecificationError
from vrailang.specs import CURRENT_SPEC_STATE
from vrailang.dataconstraints import srid, length
from models import BaseExtent, BaseValueDomain

if TYPE_CHECKING:
    from vrailang.featureclasses import feature
    from vrailang.datatypes import DataType
    from vrailang.specs import ValidationTheme

NO_VALIDATION_CODE = 'VALIDATION_CODE_NOT_SET'


@dataclass
class ValidationRule:
    """A validation rule is identified by a validation code 
    and describes which validator needs to be run and how it needs to be run.
    """

    validator: Type[AbstractValidator]
    validation_code: str
    severity: str
    feature_class: Type['feature']
    args: tuple
    kwargs: dict

    theme: 'ValidationTheme' = field(init=False)

    def __post_init__(self):
        self.theme = None  # type: ignore # Initialized by _create_rule_and_register

    def TreatAsWarning(self) -> Self:
        return self._set_severity('WARNING')

    def TreatAsStatistic(self) -> Self:
        return self._set_severity('STATISTIC')

    def _set_severity(self, severity: str) -> Self:
        self.severity = severity

        if self.validation_code == NO_VALIDATION_CODE:
            _set_validation_code_via_assignment(self, frame=3)

        return self

    def run(self, run_id: int, arg_loader: ArgLoader):
        # Convert vrailang.feature to QgsVectorLayer in featureclass, *args and **kwargs.
        feature_layer = arg_loader(self.feature_class)
        self.args = tuple([arg_loader(a) for a in list(self.args)])

        for key in self.kwargs:
            self.kwargs.update({key: arg_loader(self.kwargs[key])})

        self.validator.run(run_id, self.validation_code, self.severity, feature_layer, *self.args, **self.kwargs)

    @property
    def HasValidationCode(self) -> bool:
        return self.validation_code is not None and self.validation_code != NO_VALIDATION_CODE


def _create_rule_and_register(
        validator: Type[AbstractValidator],
        feature_class: Union[Type['feature'], Type[FeatureclassProtocol]],
        args: tuple,
        kwargs: dict[str, Any]
) -> ValidationRule:
    feature_class = cast(Type['feature'], feature_class)

    # Create rule and set validation code, if possible
    rule = ValidationRule(validator, NO_VALIDATION_CODE, 'ERROR', feature_class, args, kwargs)
    _set_validation_code_via_assignment(rule)

    cur_theme = CURRENT_SPEC_STATE.current_theme
    if cur_theme is None:
        raise VraiSpecificationError('A rule must be defined between begin_theme() and end_theme()')
    else:
        cur_theme.add_validation_rule(rule)
        rule.theme = cur_theme

    return rule


def _set_validation_code_via_assignment(obj, frame=3):
    if not hasattr(obj, 'var'):
        fv = FastVarname(depth=frame + 1)
        name = fv.varname
        if name is not None:
            obj.validation_code = name


_DataType = TypeVar('_DataType', bound='DataType')
class MixinAttributeRules(Generic[_DataType], FeatureclassAttributeProtocol[_DataType]):
    def MustNotBeNull(self) -> ValidationRule:
        return _create_rule_and_register(
            validators.AttributeNotNullValidator,
            self.featureclass,
            (self.name,),
            {}
        )

    def MustNotBeEmpty(self) -> ValidationRule:
        return _create_rule_and_register(
            validators.AttributeNotEmptyValidator,
            self.featureclass,
            (self.name,),
            {}
        )

    def MustNotBeUnknown(self) -> ValidationRule:
        return _create_rule_and_register(
            validators.AttributeNotUnknownValidator,
            self.featureclass,
            (self.name,),
            {}
        )

    def MustHaveCorrectCRS(self) -> ValidationRule:
        srid_constraint = self.get_constraint(srid)
        if srid_constraint is None:
            raise VraiSpecificationError('MustHaveCorrectCRS can only be used on attributes with an srid constraint.')

        return _create_rule_and_register(
            validators.CrsValidator,
            self.featureclass,
            (srid_constraint.id, self.featureclass.THEME.schema),
            {}
        )

    def MustHaveCorrectGeometryType(self) -> ValidationRule:
        return _create_rule_and_register(
            validators.GeometryTypeValidator,
            self.featureclass,
            (self.datatype.__name__,),
            {}

        )

    def MustBeOfValues(self, value_domain: Type['BaseValueDomain']) -> ValidationRule:  # TODO separator
        return _create_rule_and_register(
            validators.AllowedAttributeValidator,
            self.featureclass,
            (self.name, value_domain.to_list()),
            {}
        )

    def DetermineCompletionRate(self) -> ValidationRule:
        return _create_rule_and_register(
            validators.CompletionRateValidator,
            self.featureclass,
            ([self.name],),
            {}
        )

    def MustBeUnique(self) -> ValidationRule:
        return _create_rule_and_register(
            validators.UniqueFieldValidator,
            self.featureclass,
            (self.name, self.featureclass.THEME.schema),
            {}
        )


class MixinFeatureclassRules(FeatureclassProtocol):

    @classmethod
    def CreateDebugRule(cls) -> ValidationRule:
        return _create_rule_and_register(
            validators.DebugFeatureValidator,
            cls,
            (),
            {}
        )

    @classmethod
    def MustComplyWithDataschema(cls) -> ValidationRule:
        attr_dict = {}
        for key, value in cls.ATTRIBUTES.items():
            length_constraint = value.get_constraint(length)
            length_constraint_value = length_constraint.value if length_constraint else None
            attr_dict[key] = (value.datatype.as_string(), length_constraint_value)

        return _create_rule_and_register(
            validators.DataSchemaValidator,
            cls,
            (attr_dict, cls.THEME.schema),
            {}
        )

    @classmethod
    def MustHaveValidGeometry(cls) -> ValidationRule:
        return _create_rule_and_register(
            validators.ValidGeometryValidator,
            cls,
            (),
            {}
        )

    @classmethod
    def MustBeWithinExtent(cls, extent: 'BaseExtent') -> ValidationRule:
        return _create_rule_and_register(
            validators.ExtentValidator,
            cls,
            (extent,),
            {}
        )

    @classmethod
    def LengthMustBeAtLeast(cls, minimum_length, check_multilines_per_linestring=False) -> ValidationRule:
        return _create_rule_and_register(
            validators.MinimumLengthValidator,
            cls,
            (minimum_length,),
            {}
        )

    @classmethod
    def MustBeInsideMatchingArea(cls, area_feature_class: Type['feature'], id_field: str) -> ValidationRule:
        return _create_rule_and_register(
            validators.FeatureAreaIdentifierConsistencyValidator,
            cls,
            (area_feature_class, id_field),
            {}
        )

    @classmethod
    def AreaMustBeAtLeast(cls, minimum_area: Union[int, float]) -> ValidationRule:
        return _create_rule_and_register(
            validators.MinimumAreaValidator,
            cls,
            (minimum_area,),
            {}
        )

    @classmethod
    def VerticesDistanceMustBeAtLeast(cls, minimum_distance: Union[int, float]) -> ValidationRule:
        return _create_rule_and_register(
            validators.MinimumVertexDistanceValidator,
            cls,
            (minimum_distance,),
            {}
        )

    @classmethod
    def MustNotHaveDangles(cls) -> ValidationRule:
        return _create_rule_and_register(
            validators.MustNotHaveDanglesValidator,
            cls,
            (),
            {}
        )

    @classmethod
    def MustNotHaveGaps(cls) -> ValidationRule:
        return _create_rule_and_register(
            validators.MustNotHaveGapsValidator,
            cls,
            (),
            {}
        )

    @classmethod
    def MustNotHaveOverlaps(cls) -> ValidationRule:
        return _create_rule_and_register(
            validators.MustNotOverlapValidator,
            cls,
            (),
            {}
        )

    @classmethod
    def MustNotOverlapWithFeaturesOfSameType(cls, attributes: list[str]) -> ValidationRule:
        return _create_rule_and_register(
            validators.MustNotOverlapValidator,
            cls,
            (),
            {
                'type_attributes': attributes
            }
        )

    @classmethod
    def MustOverlapWith(cls, feature_class: Type['feature']) -> ValidationRule:
        return _create_rule_and_register(
            validators.MustOverlapWithValidator,
            cls,
            (feature_class,),
            {}
        )

    @classmethod
    def MustBeInside(cls, feature_class: Type['feature']) -> ValidationRule:
        return _create_rule_and_register(
            validators.MustBeInsideValidator,
            cls,
            (feature_class,),
            {}
        )

    @classmethod
    def MustBeInProximityOf(cls, feature_class: Type['feature'], distance: Union[int, float]) -> ValidationRule:
        return _create_rule_and_register(
            validators.ProximityValidator,
            cls,
            (feature_class, distance,),
            {}
        )

    @classmethod
    def AdjacentFacesMustDiffer(cls, attributes: list[str]) -> ValidationRule:
        return _create_rule_and_register(
            validators.NoAdjacentFacesSameAttributeValidator,
            cls,
            (attributes,),
            {}
        )

    @classmethod
    def DetermineFeatureCount(cls, group_by_field_1: str | None = None, group_by_field_2: str | None = None,
                              minimum_record_count: int = -1) -> ValidationRule:
        return _create_rule_and_register(
            validators.FeatureCountValidator,
            cls,
            (group_by_field_1, group_by_field_2, minimum_record_count),
            {}
        )

    @classmethod
    def DeterminePercentage(cls, group_by_field_1: str, value: Any, group_by_field_2: str | None = None) -> ValidationRule:
        return _create_rule_and_register(
            validators.FeaturePercentageValidator,
            cls,
            (group_by_field_1, value, group_by_field_2),
            {}
        )

    @classmethod
    def MustBeConsistentAcrossBorder(cls, border_feature_class: Type['feature'],
                                     consistent_attributes: list[str]) -> ValidationRule:
        return _create_rule_and_register(
            validators.AttributeAcrossBorderConsistencyValidator,
            cls,
            (border_feature_class, consistent_attributes),
            {}
        )

    @classmethod
    def MustTouchCorrespondingBoundaryOf(cls, area_feature_class: Type['feature'],
                                         corresponding_attributes: list[str]) -> ValidationRule:
        return _create_rule_and_register(
            validators.MustTouchCorrespondingBoundaryValidator,
            cls,
            (area_feature_class, corresponding_attributes),
            {}
        )
