#! /usr/bin/env python
# coding: utf-8

import sys
from pprint import pprint

def lcs(a, b):
    """
    >>> pprint(lcs('xyxxzxyzxy', 'zxzyyzxxyxxz'))
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2],
     [0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3],
     [0, 0, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 4],
     [0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5],
     [0, 1, 2, 2, 2, 2, 3, 4, 4, 4, 5, 5, 5],
     [0, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5],
     [0, 1, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6],
     [0, 1, 2, 3, 3, 3, 4, 5, 5, 5, 6, 6, 6],
     [0, 1, 2, 3, 4, 4, 4, 5, 5, 6, 6, 6, 6]]
    """
    n = len(a)
    m = len(b)
    L = [[0 for i in range(m+1)] for i in range(n+1)]
    for i in range(n):
        for j in range(m):
            if a[i] == b[j]:
                L[i+1][j+1] = L[i][j] + 1
            else:
                L[i+1][j+1] = max(L[i][j+1], L[i+1][j])
    
    return L

def matchain(r):
    """
    >>> pprint(matchain([5, 10, 4, 6, 10, 2]))
    [[0, 200, 320, 620, 348],
     [0, 0, 240, 640, 248],
     [0, 0, 0, 240, 168],
     [0, 0, 0, 0, 120],
     [0, 0, 0, 0, 0]]
    """
    n = len(r) - 1
    C = [[0 for i in range(n)] for i in range(n)]
    for d in range(1, n):
        for i in range(n-d):
            j = i + d
            C[i][j] = sys.maxint
            for k in (i+1, j):
                C[i][j] = min(C[i][j], C[i][k-1]+C[k][j]+r[i]*r[k]*r[j+1])

    return C


################################################################################

def lis(A):
    """
    >>> A = 'abdefc'
    >>> lis(A)
    5
    """
    n = len(A)
    C = [1 for i in range(n)]
    for i in range(n):
        for j in range(i):
            if A[j] < A[i] and C[j] + 1 > C[i]:
                C[i] = C[j] + 1
    
    return max(C)


def missile1(A):
    """
    >>> A = [389, 207, 155, 300, 299, 170, 158, 65]
    >>> missile1(A)
    6
    """
    n = len(A)
    C = [1 for i in range(n)]
    for i in range(n):
        for j in range(i):
            if A[j] >= A[i] and C[j] + 1 > C[i]:
                C[i] = C[j] + 1
    
    return max(C)

def missile2(A):
    """
    greedy is wrong for this, example:
    
    6 1 7 3 2 -> 6 3 2 / 1 / 7
    6 1 7 3 2 -> 6 1 / 7 3 2
    
    >>> A = [389, 207, 155, 300, 299, 170, 158, 65]
    >>> missile2(A)
    2
    """
    n = len(A)
    C = [1 for i in range(n)]
    for i in range(n):
        for j in range(i):
            if A[j] < A[i] and C[j] + 1 > C[i]:
                C[i] = C[j] + 1
    
    return max(C)


def missile(h):
    """
    f(0, inf) = max(f(1, h1) + 1, f(1, Inf))
    
    f(0, h) stands for max number of missiles[0:n] can be intercepted 
    within height h.
    
    >>> h = [389, 207, 155, 300, 299, 170, 158, 65]
    >>> C = missile(h)
    >>> pprint(C)
    [[6, 0, 0, 0, 0, 0, 0, 0],
     [5, 5, 0, 0, 0, 0, 0, 0],
     [5, 5, 3, 0, 0, 0, 0, 0],
     [5, 5, 3, 1, 0, 0, 0, 0],
     [4, 4, 3, 1, 4, 0, 0, 0],
     [3, 3, 3, 1, 3, 3, 0, 0],
     [2, 2, 2, 1, 2, 2, 2, 0],
     [1, 1, 1, 1, 1, 1, 1, 1]]
    >>> C[0][0]
    6
    """
    inf = float('inf')
    n = len(h)
    C = [[0 for i in range(n)] for i in range(n)]
    h.insert(0, inf)
    
    for i in range(0, n):
        if h[i] >= h[n]:
            C[n-1][i] = 1
        else:
            C[n-1][i] = 0

    for j in range(n-2, -1, -1):
        for i in range(j+1):
            if h[i] >= h[j+1]:
                max0 = max([e for k,e in enumerate(C[j+1][:]) if h[k] <= h[i]])
                max1 = max([e for k,e in enumerate(C[j+1][:]) if h[k] <= h[j+1]]) + 1
                C[j][i] = max(max0, max1)
            else:
                max0 = max([e for k,e in enumerate(C[j+1][:]) if h[k] <= h[i]])
                C[j][i] = max0
    
    return C

################################################################################

if __name__ == '__main__':
    import doctest
    doctest.testmod()

