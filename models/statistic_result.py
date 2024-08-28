from __future__ import annotations

from dataclasses import dataclass
from . import ValidationResult

@dataclass
class StatisticResult(ValidationResult):
    """Dataclass for storing statistic results in the database.
    
    All attributes are inherited of the abstract ValidationResult.
    """
    pass
