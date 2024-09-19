from dataclasses import dataclass

@dataclass
class BaseExtent():
    x_min: float
    y_min: float
    x_max: float
    y_max: float
