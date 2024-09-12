'''
The `vrailang.rules` module contains methods for creating `ValidationRule` objects.
These methods reside in `MixinAttributeRules` for rules pertaining to a featureclass's attributes
and in `MixinFeatureclassRules` for rules pertaining to a featureclass itself.
'''

from dataclasses import dataclass, field
from typing import Any, Type, TYPE_CHECKING, Callable, Union
from typing_extensions import Self
import varname
from validators.abstract_validator import AbstractValidator
import validators
from vrailang.errors import VraiSpecificationError
from vrailang.specs import CURRENT_SPEC_STATE
from vrailang.dataconstraints import srid, length

if TYPE_CHECKING:
    from vrailang.featureclasses import feature, FeatureclassAttribute
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
    feature_class: 'feature'
    args: tuple
    kwargs: dict

    theme: 'ValidationTheme' = field(init=False)
    
    def __post_init__(self):
        self.theme = None


    def TreatAsWarning(self) -> Self:
        return self._set_severity('WARNING')
    

    def TreatAsStatistic(self) -> Self:
        return self._set_severity('STATISTIC')


    def _set_severity(self, severity: str) -> Self:
        self.severity = severity

        if self.validation_code == NO_VALIDATION_CODE:
            _set_validation_code_via_assignment(self, frame=3)

        return self
    

    def run(self, run_id: int, arg_loader: Callable[['object'], object]):
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
        feature_class: 'feature',
        args: tuple[Any],
        kwargs: dict[str, Any]
        ) -> ValidationRule:
    
    # Create rule and set validation code, if possible
    rule = ValidationRule(validator, NO_VALIDATION_CODE, 'ERROR', feature_class, args, kwargs)
    _set_validation_code_via_assignment(rule)

    cur_theme = CURRENT_SPEC_STATE.current_theme
    if cur_theme is None:
        raise VraiSpecificationError('A rule must be defined between begin_theme() and end_theme()')
    if cur_theme is not None:
        cur_theme.add_validation_rule(rule)

    return rule

def _set_validation_code_via_assignment(obj, frame=3):
    if not hasattr(obj, 'var'):
        try:
            obj.validation_code = varname.varname(frame=frame)
        except varname.ImproperUseError as _:
            # This could happen when called from _create_rule_and_register()
            # and the rule is not assigned directly to a variable, 
            # e.g.: `Example042 = RoadLine.id.MustNotBeNull().TreatAsWarning()`
            pass


class MixinAttributeRules:
    def MustNotBeNull(self: 'FeatureclassAttribute') -> ValidationRule:
        return _create_rule_and_register(
            validators.AttributeNotNullValidator,
            self.featureclass,
            (self.name,),
            {}
        )
    
    def MustHaveCorrectCRS(self: 'FeatureclassAttribute') -> ValidationRule:
        srid_constraint = self.get_constraint(srid)
        if srid_constraint is None:
            raise VraiSpecificationError(f'MustHaveCorrectCRS can only be used on attributes with an srid constraint.')
        
        return _create_rule_and_register(
            validators.CrsValidator,
            self.featureclass,
            (srid_constraint.id, self.featureclass.THEME.schema),
            {}
        )
    
    def MustHaveCorrectGeometryType(self: 'FeatureclassAttribute') -> ValidationRule:
        return _create_rule_and_register(
            validators.GeometryTypeValidator,
            self.featureclass,
            (self.datatype.__name__,),
            {}

        )
    
    def MustBeOfValues(self: 'FeatureclassAttribute', allowed_values: list[str]) -> ValidationRule: # TODO separator
        return _create_rule_and_register(
            validators.AllowedAttributeValidator,
            self.featureclass,
            (self.name, allowed_values),
            {}
        )
    
    def CalculateCompletionRate(self: 'FeatureclassAttribute') -> ValidationRule:
        return _create_rule_and_register(
            validators.CompletionRateValidator,
            self.featureclass,
            ([self.name],),
            {}
        )



class MixinFeatureclassRules:


    @classmethod
    def MustComplyWithDataschema(cls: 'feature') -> ValidationRule:

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
    def MustHaveValidGeometry(cls: 'feature') -> ValidationRule:
        return _create_rule_and_register(
            validators.ValidGeometryValidator,
            cls,
            (),
            {}
        )
    
    
    @classmethod
    def LengthMustBeAtLeast(cls: 'feature', minimum_length, check_multilines_per_linestring=False) -> ValidationRule:
        return _create_rule_and_register(
            validators.MinimumLengthValidator,
            cls,
            (minimum_length,),
            {}
        )
    

    @classmethod
    def MustBeInsideMatchingArea(cls: 'feature', area_feature_class: 'feature', id_field: str) -> ValidationRule:
        return _create_rule_and_register(
            validators.FeatureAreaIdentifierConsistencyValidator,
            cls,
            (area_feature_class, id_field),
            {}
        )
    

    @classmethod
    def AreaMustBeAtLeast(cls: 'feature', minimum_area: Union[int, float]) -> ValidationRule:
        return _create_rule_and_register(
            validators.MinimumAreaValidator,
            cls,
            (minimum_area,),
            {}
        )

    
    @classmethod
    def VerticesDistanceMustBeAtLeast(cls: 'feature', minimum_distance: Union[int, float]) -> ValidationRule:
        return _create_rule_and_register(
            validators.MinimumVertexDistanceValidator,
            cls,
            (minimum_distance,),
            {}
        )

