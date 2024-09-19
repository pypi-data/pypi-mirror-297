"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to the binary tree.
"""

class BinaryTree:
    """Defines a binary tree."""
    def __init__(self, val):
        self._value = val
        self._left = None
        self._right = None

    """Inserts a node as a left child."""
    def insert_left(self, val):
        n = BinaryTree(val)
        # this node doesn't have a left child
        if (self._left == None):
            self._left = n
        # this node already has a left child
        else:
            n._left = self._left
            self._left = n

    """Inserts a node as a right child."""
    def insert_right(self, val):
        n = BinaryTree(val)
        # this node doesn't have a right child
        if (self._right == None):
            self._right = n
        # this node already has a right child
        else:
            n._right = self._right
            self._right = n

    """Returns the value of a node."""
    def get_value(self):
        return self._value

    """Sets the value of a node."""
    def set_value(self, val):
        self._value = val

    """Returns the left child of a node."""
    def get_left(self):
        return self._left

    """Returns the right child of a node."""
    def get_right(self):
        return self._right

    """Set getters and setters."""
    value = property(get_value, set_value)
    left = property(get_left)
    right = property(get_right)

    """Displays the tree "sideways"."""
    def print_tree(self, level=0):
        if (self != None):
            if (self.right):
                self.right.print_tree(level + 1)
            print(f"{'    ' * level}{self.value}")
            if (self.left):
                self.left.print_tree(level + 1)

