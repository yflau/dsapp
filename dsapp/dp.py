#! /usr/bin/env python
# coding: utf-8

"""
Dynamic programming.

Reference:

- Introduction to Algorithms.
- http://wenku.baidu.com/view/f8ccea120b4e767f5acfce83.html
- http://blog.csdn.net/dingyaguang117/article/details/5836918

"""

import sys
from itertools import chain
from pprint import pprint

INF = float('inf')


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

### 1. Longest sub-sequence

def lss(A, type = '<'):
    """
    Longest sub-sequence.
    
    type : ['<', '<=', '>', '>=']
    
    >>> A = 'abdefc'
    >>> DP, N = lss(A)
    >>> max(DP)
    5
    >>> A = [1,16,17,18,20,10,22,22,8,17,26,14,3,24,8,1,2,21,2,17]
    >>> DP, N = lss(A, '>')
    >>> A
    [1, 16, 17, 18, 20, 10, 22, 22, 8, 17, 26, 14, 3, 24, 8, 1, 2, 21, 2, 17]
    >>> DP
    [1, 1, 1, 1, 1, 2, 1, 1, 3, 2, 1, 3, 4, 2, 4, 5, 5, 3, 5, 4]
    >>> N
    [1, 1, 1, 1, 1, 4, 1, 1, 4, 3, 1, 3, 7, 1, 3, 10, 10, 1, 10, 1]
    >>> A = [9, 7, 5, 8, 5, 1]
    >>> DP, N = lss(A, '>')
    >>> DP
    [1, 2, 3, 2, 3, 4]
    >>> N
    [1, 1, 1, 1, 2, 2]
    """
    if type not in ['<', '<=', '>', '>=']:
        type = '<'
    
    #A.append({'<':INF, '<=':INF, '>':-INF, '>=':-INF}.get(type))
    n = len(A)
    DP = [1 for i in range(n)]
    N = [1 for i in range(n)]
    
    for i in range(1, n):
        V = {}
        for j in range(i-1, -1, -1):
            if eval('A[j] %s A[i]' % type) and DP[j] + 1 >= DP[i]:
                if DP[j] + 1 > DP[i]:
                    DP[i] = DP[j] + 1
                    N[i] = N[j]
                elif DP[j] + 1 == DP[i]:
                    if not V.get(A[j], 0):
                        N[i] += N[j]
                V[A[j]] = 1
    
    return DP, N

def lss_list(DP, N, m = None):
    """
    List all index sequence of longest sub-sequences.
    
    >>> A = [9, 8, 7, 6, 2, 6, 5]
    >>> DP, N = lss(A, '>')
    >>> lss_list(DP, N)
    [[0, 1, 2, 5, 6], [0, 1, 2, 3, 4]]
    >>> A = [9, 7, 5, 8, 5, 1]
    >>> DP, N = lss(A, '>')
    >>> lss_list(DP, N)
    [[0, 3, 4, 5], [0, 1, 4, 5]]
    >>> A = [1,16,17,18,20,10,22,22,8,17,26,14,3,24,8,1,2,21,2,17]
    >>> DP, N = lss(A, '>')
    >>> result = lss_list(DP, N)
    >>> pprint(result) # doctest: +ELLIPSIS
    [[7, 9, 11, 14, 18],
     [6, 9, 11, 14, 18],
    ...
     [1, 5, 8, 12, 15]]
    """
    result = []
    L = len(DP)
    if m is None:
        m = max(DP)
    DP.reverse()
    N.reverse()
    indexes = [i for i,e in enumerate(DP) if e == m]
    cache = {}
    
    def find_prev(index):
        if index in cache or DP[index] == 1:
            return
        dp = DP[index]
        num = N[index]
        pis = [i for i,e in enumerate(DP) if e == dp-1 and i > index]
        n = k = 0
        while n < num:
            cache.setdefault(index, []).append(pis[k])
            n = sum([N[e] for e in cache[index]])
            k += 1
        for e in cache[index]:
            find_prev(e)
    
    for i in indexes:
        find_prev(i)
        ii = [[i]]
        iitem = [[i]*N[i]]
        
        for j in range(m-1, 0, -1):
            tmp = []
            for k in ii[-1]:
                tmp.extend(cache[k])
            flat = [[e]*N[e] for e in tmp]
            iitem.append(list(chain(*flat)))
            ii.append(tmp)
            
        result.extend([map(lambda e: L-e-1, e)[::-1] for e in zip(*iitem)])
        
    return result

def lss_pprint(A, indexlist, width = 3):
    """
    Pretty print longest sub-sequences.
    
    >>> A = [9, 7, 5, 8, 5, 1]
    >>> DP, N = lss(A, '>')
    >>> result = lss_list(DP, N)
    >>> lss_pprint(A, result) # doctest: +NORMALIZE_WHITESPACE
    9  7  5  8  5  1
    9  -  -  8  5  1
    9  7  -  -  5  1
    >>> A = [1,16,17,18,20,10,22,22,8,17,26,14,3,24,8,1,2,21,2,17]
    >>> DP, N = lss(A, '>')
    >>> result = lss_list(DP, N)
    >>> lss_pprint(A, result) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    1  16 17 18 20 10 22 22 8  17 26 14 3  24 8  1  2  21 2  17
    -  -  -  -  -  -  -  22 -  17 -  14 -  -  8  -  -  -  2  -
    -  -  -  -  -  -  22 -  -  17 -  14 -  -  8  -  -  -  2  -
    ...
    -  16 -  -  -  10 -  -  8  -  -  -  3  -  -  1  -  -  -  -
    """
    print ''.join([str(e).ljust(width) for e in A])
    for e in indexlist:
        tmp = [a if i in e else '-' for i,a in enumerate(A) ]
        print ''.join([str(e).ljust(width) for e in tmp])

### examples for Longest sub-sequence

def missile1(A):
    """
    >>> A = [389, 207, 155, 300, 299, 170, 158, 65]
    >>> missile1(A)
    6
    >>> DP, N = lss(A, '>=')
    >>> DP
    [1, 2, 3, 2, 3, 4, 5, 6]
    >>> N
    [1, 1, 1, 1, 1, 1, 1, 1]
    >>> max(DP)
    6
    >>> lss_list(DP, N)
    [[0, 3, 4, 5, 6, 7]]
    """
    n = len(A)
    DP = [1 for i in range(n)]
    
    for i in range(n):
        for j in range(i):
            if A[j] >= A[i] and DP[j] + 1 > DP[i]:
                DP[i] = DP[j] + 1
    
    return max(DP)

def missile2(A):
    """
    greedy is wrong for this, example:
    
    6 1 7 3 2 -> 6 3 2 / 1 / 7
    6 1 7 3 2 -> 6 1 / 7 3 2
    
    >>> A = [389, 207, 155, 300, 299, 170, 158, 65]
    >>> missile2(A)
    2
    >>> DP, N = lss(A)
    >>> max(DP)
    2
    """
    n = len(A)
    DP = [1 for i in range(n)]
    
    for i in range(n):
        for j in range(i):
            if A[j] < A[i] and DP[j] + 1 > DP[i]:
                DP[i] = DP[j] + 1
    
    return max(DP)


def missile(h):
    """
    Top-down method.
    
    f(0, inf) = max(f(1, h1) + 1, f(1, Inf))
    
    f(0, h) stands for max number of missiles[0:n] can be intercepted 
    within height h.
    
    >>> h = [389, 207, 155, 300, 299, 170, 158, 65]
    >>> DP = missile(h)
    >>> pprint(DP)
    [[6, 0, 0, 0, 0, 0, 0, 0],
     [5, 5, 0, 0, 0, 0, 0, 0],
     [5, 5, 3, 0, 0, 0, 0, 0],
     [5, 5, 3, 1, 0, 0, 0, 0],
     [4, 4, 3, 1, 4, 0, 0, 0],
     [3, 3, 3, 1, 3, 3, 0, 0],
     [2, 2, 2, 1, 2, 2, 2, 0],
     [1, 1, 1, 1, 1, 1, 1, 1]]
    >>> DP[0][0]
    6
    """
    inf = float('inf')
    n = len(h)
    DP = [[0 for i in range(n)] for i in range(n)]
    h.insert(0, inf)
    
    for i in range(0, n):
        if h[i] >= h[n]:
            DP[n-1][i] = 1
        else:
            DP[n-1][i] = 0

    for j in range(n-2, -1, -1):
        for i in range(j+1):
            if h[i] >= h[j+1]:
                max0 = max([e for k,e in enumerate(DP[j+1][:]) if h[k] <= h[i]])
                max1 = max([e for k,e in enumerate(DP[j+1][:]) if h[k] <= h[j+1]]) + 1
                DP[j][i] = max(max0, max1)
            else:
                max0 = max([e for k,e in enumerate(DP[j+1][:]) if h[k] <= h[i]])
                DP[j][i] = max0
    
    return DP

def chorus(A):
    """
    Note: no requrement: i-1 == k-i
    
    >>> A = [186, 186, 150, 200, 160, 130, 197, 220]
    >>> DP, N = lss(A)
    >>> DP
    [1, 1, 1, 2, 2, 1, 3, 4]
    >>> DP, N = lss(A, '>')
    >>> DP
    [1, 1, 2, 1, 2, 3, 2, 1]
    >>> chorus(A)
    4
    """
    n = len(A)
    lt, N = lss(A)
    gt, N = lss(A, '>')
    tmp = max([lt[i] + gt[i] for i in range(n)])
    
    return n - tmp + 1

def buylow(A):
    """
    Sum(num[j]) when dp[j]==dp[i]-1 and A[j] > A[i]
    
    Reference:
    
    - http://blog.csdn.net/dingyaguang117/article/details/5836918
    
    >>> A = [68, 69, 54, 64, 68, 64, 70, 67, 78, 62, 98, 87]
    >>> buylow(A)
    (4, 2)
    >>> DP, N = lss(A, '>')
    >>> DP
    [1, 1, 2, 2, 2, 3, 1, 3, 1, 4, 1, 2]
    >>> N
    [1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1]
    >>> DP, N = lss(A, '>')
    >>> result = lss_list(DP, N)
    >>> lss_pprint(A, result) # doctest: +NORMALIZE_WHITESPACE
    68 69 54 64 68 64 70 67 78 62 98 87
    -  69 -  -  68 -  -  67 -  62 -  -
    -  69 -  -  68 64 -  -  -  62 -  -
    """
    DP, N = lss(A, '>')
    m = max(DP)
    indexes = [i for i,e in enumerate(DP) if e == m]
    nc = sum([N[i] for i in indexes])

    return m, nc

################################################################################

if __name__ == '__main__':
    import doctest
    doctest.testmod()