"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to the deque.
"""

from CSC201UT.UnorderedList import UnorderedList

class Deque():
    """Defines a deque."""
    def __init__(self):
        self._dq = UnorderedList()

    """Adds an item to the front of the deque."""
    def add_front(self, item):
        self._dq.append(item)

    """Adds an item to the rear of the deque."""
    def add_rear(self, item):
        self._dq.add(item)

    """Removes an item from the front of the deque."""
    def remove_front(self):
        return self._dq.pop()

    """Removes an item from the rear of the deque."""
    def remove_rear(self):
        return self._dq.pop(0)

    """Returns if the deque is empty."""
    def is_empty(self):
        return self._dq.is_empty()

    """Returns the deque's size."""
    def size(self):
        return self._dq.size()

    """Returns the deque as a string."""
    def __str__(self):
        return self._dq.__str__()

