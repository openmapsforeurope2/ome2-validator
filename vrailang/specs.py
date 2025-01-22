'''
The `vrailang.specs` module contains bookkeeping logic for declaring validation specifications and validation themes
via the functions `begin_spec`/`end_spec` and `begin_theme`/`end_theme`.
'''

from dataclasses import dataclass, field
from typing import ClassVar, Union, TYPE_CHECKING, Callable
from models import ValidationParameters
from vrailang.errors import VraiSpecificationError
import logging
from logging import Logger

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


    def featureclass(self, name: str) -> 'feature':
        if name not in self.feature_classes:
            raise VraiSpecificationError(f'Featureclass {name} cannot be retrieved from theme {self.name}: it is not part of this theme')    
        
        return self.feature_classes[name]
        

@dataclass
class ValidationSpecification:
    name: str
    themes: dict[str, ValidationTheme] = field(init=False)

    ALL_SPECIFICATIONS: ClassVar[dict[str, 'ValidationSpecification']] = {}
    logger: Logger = logging.getLogger(__name__)

    def __post_init__(self):
        self.themes = {}


    def run(self, params: ValidationParameters, arg_loader: Callable[['object'], object]):
        for validation_theme in self.themes.values():
            # Skip disabled themes
            if not params.theme_is_enabled(validation_theme.name):
                self.logger.info(f"Skipping theme {validation_theme.name} since it is not enabled.")
                continue

            for validation_rule in validation_theme.validation_rules.values():
                # Skip disabled checks
                if not params.check_is_enabled(validation_rule.validation_code):
                    self.logger.info(f"Skipping check {validation_rule.validation_code} since it is not enabled.")
                    continue

                validation_rule.run(params.run_id, arg_loader)

    def theme(self, name: str) -> 'ValidationTheme':
        if name not in self.themes:
            raise VraiSpecificationError(f'Theme {name} cannot be retrieved from specification {self.name}: it is not part of this specification')    
        
        return self.themes[name]


@dataclass
class CurrentSpecState:
    name: Union[None, str] = None

    current_theme: Union[None, ValidationTheme] = None
    known_themes: dict[str, ValidationTheme] = None  # type: ignore # Correctly initialized in __post_init__

    def __post_init__(self):
        self.known_themes = {}


CURRENT_SPEC: Union[None, ValidationSpecification] = None
CURRENT_SPEC_STATE = CurrentSpecState()


def begin_theme(name: str, schema: str | None = None):
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

