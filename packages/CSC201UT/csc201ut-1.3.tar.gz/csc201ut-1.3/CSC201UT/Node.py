"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to the list node.
"""

class Node:
    """Defines a list node."""
    def __init__(self, data):
        self._data = data
        self._link = None

    """Returns the node's data component."""
    def get_data(self):
        return self._data

    """Sets the node's data component."""
    def set_data(self, data):
        self._data = data

    """Returns the node's link component."""
    def get_link(self):
        return self._link

    """Sets the node's link component."""
    def set_link(self, link):
        self._link = link

    """Set the getters and setters."""
    data = property(get_data, set_data)
    link = property(get_link, set_link)

    """Returns a node as a string."""
    def __str__(self):
        return str(self._data)

