#! /usr/bin/env python
# coding: utf-8

import random

def select(a, k = None):
    """select algorithm.
    >>> a = range(1, 61)
    >>> select(a, 57)
    57
    >>> a = range(1, 10)
    >>> select(a)
    5
    """
    p = len(a)
    if k is None:
        k = (p+1)/2
    if p < 44:
        return sorted(a)[k-1]
    q = p/5
    M = []
    mi = q/2
    for i in range(q):
        M.append(sorted(a[5*i:5*i+5])[2])
    
    mm = select(M, mi)
    A1 = []
    A2 = [mm]
    A3 = []
    for e in a:
        if e < mm:
            A1.append(e)
        elif e > mm:
            A3.append(e)
        else:
            pass
    
    n1 = len(A1)
    if n1 >= k:
        return select(A1, k)
    elif n1 + 1 >= k:
        return mm
    else:
        return select(A3, k-n1-1)

def rselect(a, k = None):
    """random select algorithm.
    >>> a = range(1, 61)
    >>> rselect(a, 57)
    57
    >>> a = range(1, 10)
    >>> rselect(a)
    5
    """
    if k is None:
        k = (len(a)+1)/2
        
    v = random.choice(a)
    
    A1 = []
    A2 = [v]
    A3 = []
    
    for e in a:
        if e < v:
            A1.append(e)
        elif e > v:
            A3.append(e)
        else:
            pass

    n1 = len(A1)
    if n1 >= k:
        return rselect(A1, k)
    elif n1 + 1 >= k:
        return v
    else:
        return rselect(A3, k-n1-1)

def rpartition(A, pivot = None):
    """
    Randomized select element as pivot, ok.
    
    >>> A = [9, 3, 7, 2, 8, 5, 1, 0, 8]
    >>> rpartition(A, 3)
    2
    >>> A
    [1, 0, 2, 7, 8, 5, 9, 3, 8]
    """
    high = len(A)
    if pivot is None:
        pivot = random.randint(0, high-1)
    i = 0
    x = A[pivot]
    for j in range(high):
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

def qselect(a, k = None):
    """quick select algorithm.
    >>> a = range(1, 9)
    >>> qselect(a, 5)
    5
    >>> a = range(1, 10)
    >>> qselect(a)
    5
    """
    if k is None:
        k = (len(a)+1)/2
    pivot = rpartition(a)+1

    if k < pivot:
        return qselect(a[:pivot-1], k)
    elif k > pivot:
        return qselect(a[pivot:], k-pivot)
    else:
        return a[pivot-1]

def test():
    """
    Profile result:
    
     select:
      6699999
      20.5780000687
     rselect:
      6699999
      7.54699993134
     qselect:
      6699999
      4.48400020599
    """
    import time
    a = range(10000000)
    random.shuffle(a)
    print 'start...'
    t0 = time.time()
    print select(a, 6700000)
    t1 = time.time()
    print t1-t0
    print rselect(a, 6700000)
    t2 = time.time()
    print t2-t1
    print qselect(a, 6700000)
    print time.time() - t2


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #test()
