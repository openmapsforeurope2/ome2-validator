from __future__ import annotations

from dataclasses import dataclass
from . import ValidationResult

@dataclass
class GenericResult(ValidationResult):
    """Dataclass for storing generic results in the database.
    
    All attributes are inherited of the abstract ValidationResult.
    """
    pass
