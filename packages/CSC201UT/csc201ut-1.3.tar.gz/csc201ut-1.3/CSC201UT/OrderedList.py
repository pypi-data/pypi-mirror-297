"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to the ordered list.
"""

from CSC201UT.Node import Node

class OrderedList:
    """Defines an ordered list."""
    def __init__(self):
        self._head = None

    """Adds an item to the list."""
    def add(self, item):
        temp = Node(item)
        current = self._head
        previous = None

        # traverse the list
        while (current != None and current._data < item):
            # go to the next node
            previous = current
            current = current._link

        # the item should be added at the head of the list
        if (previous == None):
            temp._link = self._head
            self._head = temp
        # otherwise, it belongs somewhere else in the list
        else:
            # make the link connections
            temp._link = current
            previous._link = temp

    """Returns if the list is empty."""
    def is_empty(self):
        return (self._head == None)

    """Returns the list's size."""
    def size(self):
        num = 0
        current = self._head

        # traverse the list
        while (current != None):
            num += 1
            current = current._link

        return num

    """Searches the list for a value."""
    def search(self, value):
        current = self._head

        while (current != None):
            if (current._data == value):
                return True
            if (current._data > value):
                return False
            current = current._link

        return False

    """Removes an item from the list."""
    def remove(self, value):
        current = self._head
        previous = None

        # traverse the list
        while (current != None):
            # the value is found at current
            if (current._data == value):
                break
            # go to the next node
            previous = current
            current = current._link

        # the value wasn't found
        if (current == None):
            raise ValueError(f"{value} is not in the list!")

        # the item is at the head of the list
        if (previous == None):
            # just change the head
            self._head = current._link
        # otherwise, it's somewhere else in the list
        else:
            # route around the removed node
            previous._link = current._link

    """Returns the list as a string."""
    def __str__(self):
        s = ""
        current = self._head

        # traverse the list
        while (current != None):
            s += f"{current._data} "
            current = current._link

        return s

    """Returns an iterator for the list."""
    def __iter__(self):
        return OrderedListIterator(self._head)

class OrderedListIterator:
    """Defines an iterator for the ordered list."""
    def __init__(self, head):
        self._curr = head

    """Returns the iterator."""
    def __iter__(self):
        return self

    """Traverses to the next node and returns its value."""
    def __next__(self):
        if (not self._curr):
            raise StopIteration
        value = self._curr._data
        self._curr = self._curr._link

        return value

