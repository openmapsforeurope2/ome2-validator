from models import BaseExtent

class Epsg3035BoundsExtent(BaseExtent):
    # See https://epsg.io/3035
    x_min: float = 1_896_628.62
    y_min: float = 1_095_703.18
    x_max: float = 7_104_179.2
    y_max: float = 6_882_401.15
