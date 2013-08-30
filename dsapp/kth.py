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

def partition(A, pivot = None):
    """
    Randomized select element as pivot, ok.
    
    >>> A = [9, 3, 7, 2, 8, 5, 1, 0, 8]
    >>> partition(A, 3)
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

def ipartition(A, p = None, r = None, pivot = None):
    """
    Inplace randomized select element as pivot, memory efficient.
    
    >>> A = [9, 3, 7, 2, 8, 5, 1, 0, 8]
    >>> ipartition(A, 0, 8, 3)
    2
    >>> A
    [1, 0, 2, 7, 8, 5, 9, 3, 8]
    """
    if p is None:
        p = 0
    if r is None:
        r = len(A)-1
    if pivot is None:
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

def qselect(a, k = None):
    """Quick select algorithm.
    
    >>> a = range(1, 9)
    >>> qselect(a, 5)
    5
    >>> a = range(1, 10)
    >>> qselect(a)
    5
    """
    if k is None:
        k = (len(a)+1)/2
    pivot = partition(a)+1

    if k < pivot:
        return qselect(a[:pivot-1], k)
    elif k > pivot:
        return qselect(a[pivot:], k-pivot)
    else:
        return a[pivot-1]


def iqselect(a, k = None, p = None, r = None):
    """
    Inplace quick select algorithm, compare to qselect, this one:
    
     - memory efficient
     - can return absolute position in a
      
    >>> a = range(1, 9)
    >>> iqselect(a, 5)
    (5, 4)
    >>> a = range(1, 10)
    >>> iqselect(a)
    (5, 4)
    """
    n = len(a)
    if k is None:
        k = (n+1)/2
    if p is None:
        p = 0
    if r is None:
        r = n - 1
    pivot = ipartition(a, p, r)+1
    n1 = pivot-p
    if k < n1:
        return iqselect(a, k, p, pivot-2)
    elif k > n1:
        return iqselect(a, k-n1, pivot, r)
    else:
        return a[pivot-1], pivot - 1

def test():
    """
    Profile result:
    
     a : 165 MB
        
     select:
      result: 6699999
      time  : 20.5780000687
      memory: 285 MB
     rselect:
      result: 6699999
      time  : 7.54699993134
      memory: 303 MB
     qselect:
      result: 6699999
      time  : 4.48400020599
      memory: 326 MB
     iqselect:
      result: 6699999
      time  : 7.15599989891
      memory: 285 MB
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
    t3 = time.time()
    print t3-t2
    print iqselect(a, 6700000)
    print time.time() - t3


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #test()
