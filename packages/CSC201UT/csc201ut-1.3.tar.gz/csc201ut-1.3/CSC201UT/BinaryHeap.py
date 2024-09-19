"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to the binary heap.
"""

class BinaryHeap:
    """Defines a binary heap."""
    def __init__(self, max_heap=True):
        self._heap = []
        self._max_heap = max_heap

    """Percolates a node up the heap."""
    def _perc_up(self, i):
        while ((i - 1) // 2 >= 0):
            p = (i - 1) // 2
            if ((self._max_heap and self._heap[i] > self._heap[p]) or
                    (not self._max_heap and self._heap[i] < self._heap[p])):
                self._heap[i], self._heap[p] = self._heap[p], self._heap[i]
            i = p

    """Inserts a node into the heap."""
    def insert(self, val):
        self._heap.append(val)
        self._perc_up(len(self._heap) - 1)

    """Percolates a node down the tree."""
    def _perc_down(self, i):
        while (2 * i + 1 < len(self._heap)):
            c1 = 2 * i + 1
            c2 = 2 * i + 2
            if (c2 >= len(self._heap)):
                c = c1
            elif ((self._max_heap and self._heap[c1] > self._heap[c2]) or
                        (not self._max_heap and self._heap[c1] < self._heap[c2])):
                c = c1
            else:
                c = c2
            if ((self._max_heap and self._heap[i] < self._heap[c]) or
                    (not self._max_heap and self._heap[i] > self._heap[c])):
                self._heap[i], self._heap[c] = self._heap[c], self._heap[i]
            i = c

    """Deletes a node from the tree."""
    def delete(self):
        self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]
        val = self._heap.pop()
        self._perc_down(0)

        return val

    """Creates a heap from a list of values."""
    def heapify(self, lst):
        self._heap = lst[:]
        i = len(self._heap) // 2 - 1
        while (i >= 0):
            self._perc_down(i)
            i -= 1

    """Returns if the heap is empty."""
    def is_empty(self):
        return (len(self._heap) == 0)

    """Displays the heap as a tree."""
    def print_heap(self, i=0, level=0):
        if (len(self._heap) > 0):
            c1 = 2 * i + 1
            c2 = 2 * i + 2
            if (c2 < len(self._heap)):
                self.print_heap(c2, level + 1)
            print(f"{'    ' * level}{self._heap[i]}")
            if (c1 < len(self._heap)):
                self.print_heap(c1, level + 1)

    """Displays the heap as a list."""
    def __str__(self):
        return str(self._heap)

