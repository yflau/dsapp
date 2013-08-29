#! /usr/bin/env python
# coding: utf-8

import random

################################# QUICKSORT ####################################

def split(A):
    """
    Select first as pivot, bad for ordered data!!!
    
    >>> A = [8, 9, 3, 7, 2, 5, 1, 0, 8]
    >>> split(A)
    7
    >>> A
    [8, 3, 7, 2, 5, 1, 0, 8, 9]
    """
    high = len(A)
    i = 0
    x = A[0]
    for j in range(1, high):
        if A[j] <= x:
            i += 1
            if i != j:
                tmp = A[i]
                A[i] = A[j]
                A[j] = tmp
    tmp = A[0]
    A[0] = A[i]
    A[i] = tmp
    
    return i

def partition(A, p, r):
    """
    Select last element as pivot, bad for ordered data!!!
    
    >>> A = [9, 3, 7, 2, 8, 5, 1, 0, 8]
    >>> partition(A, 0, 8)
    7
    >>> A
    [3, 7, 2, 8, 5, 1, 0, 8, 9]
    """
    x = A[r]
    i = p
    for j in xrange(p, r):
        if A[j] <= x:
            tmp = A[i]
            A[i] = A[j]
            A[j] = tmp
            i += 1
    tmp = A[i]
    A[i] = A[r]
    A[r] = tmp
    
    return i

def rpartition(A, p, r):
    """
    Randomized select element as pivot, always OK.
    """
    pivot = random.randint(p, r)
    i = p
    x = A[pivot]
    for j in xrange(p, r+1):
        if j == pivot:
            continue
        if A[j] <= x:
            if i != j:
                if i == pivot:
                    pivot = j
                tmp = A[i]
                A[i] = A[j]
                A[j] = tmp
            i += 1
    tmp = A[pivot]
    A[pivot] = A[i]
    A[i] = tmp
    
    return i

def quicksort(A, p, r):
    """
    >>> A = [9, 3, 7, 2, 8, 5, 1, 0, 8]
    >>> quicksort(A, 0, 8)
    >>> A
    [0, 1, 2, 3, 5, 7, 8, 8, 9]
    """
    if p < r:
        #q = rpartition(A, p, r)
        q = rpartition(A, p, r)
        quicksort(A, p, q-1)
        quicksort(A, q+1, r)

################################ INSERTIONSORT #################################

def insertionsort(A):
    """
    >>> A = [9, 3, 7, 2, 5, 1, 0, 8]
    >>> insertionsort(A)
    >>> A
    [0, 1, 2, 3, 5, 7, 8, 9]
    """
    for j in xrange(1, len(A)):
        key = A[j]
        i = j - 1
        while i >= 0 and A[i] > key:
            tmp = A[i+1]
            A[i+1] = A[i]
            i -= 1
        A[i+1] = key

############################### SELECTIONSORT ##################################

def selectionsort(A):
    """
    >>> A = [9, 3, 7, 2, 5, 1, 0, 8]
    >>> selectionsort(A)
    >>> A
    [0, 1, 2, 3, 5, 7, 8, 9]
    """
    for i in xrange(0, len(A)-1):
        for j in xrange(i+1, len(A)):
            if A[j] < A[i]:
                tmp = A[j]
                A[j] = A[i]
                A[i] = tmp

################################# MERGESORT ####################################

def merge(A, p, q, r):
    alist = []
    i = p
    j = q
    while 1:
        if A[i] < A[j]:
            alist.append(A[i])
            i += 1
        else:
            alist.append(A[j])
            j +=1
        if i >= q:
            alist.extend(A[j:r])
            break
        if j >= r:
            alist.extend(A[i:q])
            break
            
    for i in xrange(len(alist)):
        A[p+i] = alist[i]
    
    return alist

def mergesort(A, p, r):
    """
    >>> A = [9, 3, 7, 2, 5, 1, 0, 8]
    >>> mergesort(A, 0, 8)
    >>> A
    [0, 1, 2, 3, 5, 7, 8, 9]
    """
    if p < r-1:
        q = int((p+r)/2.)
        mergesort(A, p, q)
        mergesort(A, q, r)
        merge(A, p, q, r)


################################################################################

if __name__ == '__main__':
    import doctest
    doctest.testmod()
