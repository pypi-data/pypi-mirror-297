"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to the stack.
"""

from CSC201UT.UnorderedList import UnorderedList

class Stack:
    """Defines a stack."""
    def __init__(self):
        self._s = UnorderedList()

    """Adds an item to the top of the stack."""
    def push(self, item):
        self._s.append(item)

    """Removes the item from the top of the stack."""
    def pop(self):
        return self._s.pop()

    """Returns the value of the item at the top of the stack."""
    def peek(self):
        if (self._s._tail == None):
            return None
        return self._s._tail._data

    """Returns if the stack is empty."""
    def is_empty(self):
        return self._s.is_empty()

    """Returns the stack's size."""
    def size(self):
        return self._s.size()

    """Returns the stack as a string."""
    def __str__(self):
        return str(self._s)

