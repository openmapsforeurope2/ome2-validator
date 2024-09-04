'''
The `vrailang.errors` module contains exception types that modules in the `vrailang` package can throw.
'''

class VraiError(Exception):
    pass

class VraiSpecificationError(VraiError):
    pass
