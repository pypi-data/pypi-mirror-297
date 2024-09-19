"""
Python utilities used in CSC 201 at UT.
This file includes classes and methods related to various sorting algorithms.
"""

from random import randint

VALUES = 500

"""the bubble sort."""
def bubble_sort(t="random"):
    # generate the appropriate list
    if (t == "random"):
        lst = [ randint(0, 999) for _ in range(VALUES) ]
    elif (t == "sorted"):
        lst = list(range(VALUES))
    else:
        lst = list(range(VALUES - 1, -1, -1))

    # sort
    for i in range(len(lst) - 1, 0, -1):
        for j in range(i):
            if (lst[j] > lst[j+1]):
                lst[j], lst[j+1] = lst[j+1], lst[j]

"""the optimized bubble sort."""
def optimized_bubble_sort(t="random"):
    # generate the appropriate list
    if (t == "random"):
        lst = [ randint(0, 999) for _ in range(VALUES) ]
    elif (t == "sorted"):
        lst = list(range(VALUES))
    else:
        lst = list(range(VALUES - 1, -1, -1))

    # sort
    for i in range(len(lst) - 1, 0, -1):
        swaps = False
        for j in range(i):
            if (lst[j] > lst[j+1]):
                swaps = True
                lst[j], lst[j+1] = lst[j+1], lst[j]
        if (not swaps):
            break

"""the selection sort."""
def selection_sort(t="random"):
    # generate the appropriate list
    if (t == "random"):
        lst = [ randint(0, 999) for _ in range(VALUES) ]
    elif (t == "sorted"):
        lst = list(range(VALUES))
    else:
        lst = list(range(VALUES - 1, -1, -1))

    # sort
    for i in range(len(lst) - 1, 0, -1):
        max_index = i
        for j in range(i):
            if (lst[j] > lst[max_index]):
                max_index = j
        lst[i], lst[max_index] = lst[max_index], lst[i]

"""the insertion sort."""
def insertion_sort(t="random"):
    # generate the appropriate list
    if (t == "random"):
        lst = [ randint(0, 999) for _ in range(VALUES) ]
    elif (t == "sorted"):
        lst = list(range(VALUES))
    else:
        lst = list(range(VALUES - 1, -1, -1))

    # sort
    for i in range(1, len(lst)):
        val = lst[i]
        j = i
        while (j > 0 and lst[j-1] > val):
            lst[j] = lst[j-1]
            j -= 1
        lst[j] = val

"""the shell sort."""
def shell_sort(t="random"):
    # generate the appropriate list
    if (t == "random"):
        lst = [ randint(0, 999) for _ in range(VALUES) ]
    elif (t == "sorted"):
        lst = list(range(VALUES))
    else:
        lst = list(range(VALUES - 1, -1, -1))
    k = len(lst) // 2

    # sort
    while (k > 0):
        for i in range(k):
            modified_insertion_sort(lst, i, k)
        k //= 2

"""the modified insertion sort (takes a k -- for the shell sort)."""
def modified_insertion_sort(lst, start, k):
    # sort
    for i in range(start + k, len(lst), k):
        val = lst[i]
        j = i
        while (j >= k and lst[j-k] > val):
            lst[j] = lst[j-k]
            j -= k
        lst[j] = val

"""the merge sort."""
def merge_sort(t="random"):
    # generate the appropriate list
    if (t == "random"):
        lst = [ randint(0, 999) for _ in range(VALUES) ]
    elif (t == "sorted"):
        lst = list(range(VALUES))
    else:
        lst = list(range(VALUES - 1, -1, -1))

    # sort
    merge(lst)

"""performs the merge function (for the merge sort)."""
def merge(lst):
    # sort
    if (len(lst) > 1):
        mid = len(lst) // 2
        left = lst[:mid]
        right = lst[mid:]
        merge(left)
        merge(right)

        l, r, i = 0, 0, 0
        while (l < len(left) and r < len(right)):
            if (left[l] <= right[r]):
                lst[i] = left[l]
                l += 1
            else:
                lst[i] = right[r]
                r += 1
            i += 1
        while (l < len(left)):
            lst[i] = left[l]
            l += 1
            i += 1
        while (r < len(right)):
            lst[i] = right[r]
            r += 1
            i += 1

"""the quick sort."""
def quick_sort(t="random"):
    # generate the appropriate list
    if (t == "random"):
        lst = [ randint(0, 999) for _ in range(VALUES) ]
    elif (t == "sorted"):
        lst = list(range(VALUES))
    else:
        lst = list(range(VALUES - 1, -1, -1))

    # sort
    quick(lst, 0, len(lst) - 1)

"""the quick sort helper function."""
def quick(lst, first, last):
    # sort
    if (first < last):
        s_point = partition(lst, first, last)
        quick(lst, first, s_point - 1)
        quick(lst, s_point + 1, last)

"""partitions a list (for the quick sort)."""
def partition(lst, first, last):
    pivot = lst[first]
    l_mark = first + 1
    r_mark = last

    while (l_mark <= r_mark):
        while (l_mark <= r_mark and lst[l_mark] <= pivot):
            l_mark += 1
        while (l_mark <= r_mark and lst[r_mark] >= pivot):
            r_mark -= 1
        if (l_mark <= r_mark):
            lst[l_mark], lst[r_mark] = lst[r_mark], lst[l_mark]
    lst[first], lst[r_mark] = lst[r_mark], lst[first]
    
    return r_mark

