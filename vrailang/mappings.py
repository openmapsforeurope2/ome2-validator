'''
The `vrailang.mappings` module contains helpers for creating mappings,
i.e., dict objects.
'''

from typing import TypeVar, Generic

__all__ = [
    'MapValues'
]

K = TypeVar("K")
V = TypeVar("V")

class MapValues(Generic[K]):
    """MapValues is a helper class for creating a dict.
    
    Args:
        *keys (K): the values that will be mapped onto another value. 

    Example:
    ```
        mapping = MapValues('a', 'b').Onto('c')
        print(mapping) # Prints: {'a': 'c', 'b': 'c'}
    ```
    """

    __slots__ = ['keys']

    def __init__(self, *keys: K) -> None:
        self.keys: tuple[K, ...] = keys

    def Onto(self, value: V) -> dict[K, V]:
        """Creates a dict in which all the given keys

        Args:
            value (V): the value to map the key values onto.

        Returns:
            dict[K, V]: the mapping of key values onto the given value.
        """
        return {key: value for key in self.keys}
