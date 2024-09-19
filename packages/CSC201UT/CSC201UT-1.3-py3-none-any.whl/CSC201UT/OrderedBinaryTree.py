"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to the ordered binary tree.
"""

class Node:
    """Defines a node."""
    def __init__(self, value):
        self._value = value
        self._left = None
        self._right = None

class OrderedBinaryTree:
    """Defines an ordered binary tree."""
    def __init__(self):
        self._root = None

    """Inserts a node into the tree."""
    def insert(self, value):
        if (not self._root):
            self._root = Node(value)
        else:
            self._insert(self._root, value)

    """The insert helper function."""
    def _insert(self, n, value):
        if (not n):
            n = Node(value)
        elif (value < n._value):
            n._left = self._insert(n._left, value)
        else:
            n._right = self._insert(n._right, value)
        return n

    """Performs a preorder traversal of the tree."""
    def preorder(self):
        return self._preorder(self._root)

    """The preorder helper function."""
    def _preorder(self, n):
        if (not n):
            return ""
        return str(n._value) + " " + self._preorder(n._left) + self._preorder(n._right)

    """Performs an inorder traversal of the tree."""
    def inorder(self):
        return self._inorder(self._root)

    """The inorder helper function."""
    def _inorder(self, n):
        if (not n):
            return ""
        return self._inorder(n._left) + str(n._value) + " " + self._inorder(n._right)

    """Performs a postorder traversal of the tree."""
    def postorder(self):
        return self._postorder(self._root)

    """The postorder helper function."""
    def _postorder(self, n):
        if (not n):
            return ""
        return self._postorder(n._left) + self._postorder(n._right) + str(n._value) + " "

    """Displays the tree as a tree."""
    def __str__(self):
        return self._str(self._root)

    """The __str__ helper function."""
    def _str(self, n, level=0):
        if (not n):
            return ""
        return self._str(n._right, level + 1) + ("\t" * level + str(n._value) + "\n") + self._str(n._left, level + 1)

