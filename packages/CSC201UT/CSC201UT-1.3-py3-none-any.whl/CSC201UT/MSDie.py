"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to the multi-sided die.
"""

from random import randint

class MSDie:
    """Defines a multi-sided die."""
    def __init__(self, sides):
        self._sides = sides
        self.roll()
        
    """Rolls the MSDie."""
    def roll(self):
        self._value = randint(1, self._sides)
        return self._value

    """Returns the MSDie as a string."""
    def __str__(self):
        return str(self._value)

    """Returns the MSDie as a string (when used in a list)."""
    def __repr__(self):
        return f"MSDie({self._sides}): {self._value}"

    """Returns if two MSDie are equal."""
    def __eq__(self, other):
        return (self._value == other._value)

    """Returns a lt comparison of two MSDie."""
    def __lt__(self, other):
        return (self._value < other._value)

    """Returns a le comparison of two MSDie."""
    def __le__(self, other):
        return (self._value <= other._value)

