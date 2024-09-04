'''
The `vrailang.specs` module contains bookkeeping logic for declaring validation specifications and validation themes
via the functions `begin_spec`/`end_spec` and `begin_theme`/`end_theme`.
'''

from dataclasses import dataclass, field
from typing import ClassVar, Union, TYPE_CHECKING

from vrailang.errors import VraiSpecificationError

if TYPE_CHECKING:
    from vrailang.rules import ValidationRule
    from vrailang.featureclasses import feature

__all__ = ['begin_spec', 'end_spec', 'begin_theme', 'end_theme', 'ValidationSpecification']


@dataclass
class ValidationTheme:
    name: str
    schema: str = field(default='public')

    validation_rules: dict[str, 'ValidationRule'] = field(init=False)
    feature_classes: dict[str, 'feature'] = field(init=False)

    def __post_init__(self):
        self.validation_rules = {}
        self.feature_classes = {}
        self._queued_validation_rules: list['ValidationRule'] = []
        self._finalized = False
    
    def add_validation_rule(self, validation_rule: 'ValidationRule'):
        if self._finalized:
            raise VraiSpecificationError('Cannot add rules to a finalized validation theme')
        
        if validation_rule.HasValidationCode:
            self.validation_rules[validation_rule.validation_code] = validation_rule
        else:
            self._queued_validation_rules.append(validation_rule)
    
    def finalize(self):
        for rule in self._queued_validation_rules:
            if rule.HasValidationCode:
                self.validation_rules[rule.validation_code] = rule
            else:
                raise VraiSpecificationError(f'Rule {rule} cannot be added to theme {self.name}: it must have a validation code')

        del self._queued_validation_rules
        self._finalized = True
        

@dataclass
class ValidationSpecification:
    name: str
    themes: dict[str, ValidationTheme] = None

    ALL_SPECIFICATIONS: ClassVar[dict[str, 'ValidationSpecification']] = {}

    def __post_init__(self):
        self.themes = {}


@dataclass
class CurrentSpecState:
    name: Union[None, str] = None

    current_theme: Union[None, ValidationTheme] = None
    known_themes: dict[str, ValidationTheme] = None

    def __post_init__(self):
        self.known_themes = {}


CURRENT_SPEC: Union[None, ValidationSpecification] = None
CURRENT_SPEC_STATE = CurrentSpecState()


def begin_theme(name: str, schema: str = None):
    if CURRENT_SPEC is None:
        raise VraiSpecificationError('Cannot create a theme without calling begin_spec() first')

    if name not in CURRENT_SPEC_STATE.known_themes:
        kwargs = {}
        if schema is not None:
            kwargs['schema'] = schema
        CURRENT_SPEC_STATE.known_themes[name] = ValidationTheme(name, **kwargs)

    theme = CURRENT_SPEC_STATE.known_themes[name]
    CURRENT_SPEC_STATE.current_theme = theme

def end_theme():
    if CURRENT_SPEC_STATE.current_theme is not None:
        CURRENT_SPEC_STATE.current_theme.finalize()
    CURRENT_SPEC_STATE.current_theme = None


def begin_spec(name: str):
    global CURRENT_SPEC
    CURRENT_SPEC = ValidationSpecification(name)


def end_spec():
    global CURRENT_SPEC
    if CURRENT_SPEC is None:
        raise VraiSpecificationError('Cannot end a validation specification without calling begin_spec() first')
    
    CURRENT_SPEC.themes = CURRENT_SPEC_STATE.known_themes
    ValidationSpecification.ALL_SPECIFICATIONS[CURRENT_SPEC.name] = CURRENT_SPEC

    CURRENT_SPEC_STATE.current_theme = None
    CURRENT_SPEC_STATE.known_themes = {}
    CURRENT_SPEC = None

