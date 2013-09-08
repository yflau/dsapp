#! /usr/bin/env python
# coding: utf-8

"""
Dynamic programming.

Reference:

- Introduction to Algorithms.
- http://wenku.baidu.com/view/f8ccea120b4e767f5acfce83.html
- http://blog.csdn.net/dingyaguang117/article/details/5836918

Problem-solving skill: Recursion + Induction

"""

import sys
from itertools import chain
import random
from pprint import pprint

#from functools32 import lru_cache

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

def rmissile(A):
    """
    Recursive method.
    
    Note: RuntimeError when length great than 1000 default.
    
    f(Inf, 0) = max(f(h0, 1) + 1, f(Inf, 1))
    f(Inf, n-1) = 1
    
    f(i, h) stands for max missiles can be contepted from the i-th missile
    with given height h.
    
    >>> A = [389, 207, 155, 300, 299, 170, 158, 65]
    >>> rmissile(A)
    6
    >>> A = [random.randint(100, 10000) for i in range(1000)]
    >>> rmissile(A) # doctest: +SKIP
    ...
    RuntimeError: maximum recursion depth exceeded
    """
    n = len(A)
    
    def f(h, i = n-1):
        if i == n-1:
            if h >= A[i]:
                return 1
            else:
                return 0
        else:
            if h >= A[i]:
                return max(f(A[i], i+1)+1, f(h, i+1))
            else:
                return f(h, i+1)
    
    return f(INF, 0)

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

def ships():
    pass

################################################################################

### 2. Knapsack problem

def pack(V, O):
    """
    NOIP 2001.
    
    State transition equation:

     f(24, 0) = 8
     f(24, 1) = max(f(24, 0), f(24-3, 0)+3)
     f(24, 2) = max(f(24, 1), f(24-12, 1)+12)
              = max(f(24, 1), f(24-12, 0)+12, f(24-12-3, 0)+12+3)
     f(24, 3) = max(f(24, 2), f(24-7, 2)+7)
              = max(f(24, 2), f(24-7, 1)+7, f(24-7-12, 1)+7+12)
              = max(f(24, 2), f(24-7, 0)+7, f(24-7-3, 0)+7+3, 
                              f(24-7-12, 0)+7+12, f(24-7-12-3, 0)+7+12+3)
     f(24, 4) = max(f(24, 3), f(24-9, 3)+9)
              = max(f(24, 3), f(24-9, 2)+9, f(24-9-7, 2)+9+7)
              = max(f(24, 3), f(24-9, 1)+9, f(24-9-12, 1)+9+12, 
                              f(24-9-7, 1)+9+7) 
                              # no f(24-9-7-12, 1)+9+7+12) for 24-9-7 < 12
              = max(f(24, 3), f(24-9, 0)+9, f(24-9-3, 0)+3,
                              f(24-9-12, 0)+9+12, f(24-9-12-3)+9+12+3,
                              f(24-9-7, 0)+9+7, f(24-9-7-3, 0)+9+7+3)

     f(v, i) stands for the most volume can be accommodated by Knapsack(v) for 
     the first i objects.
    
    >>> O = [8, 3, 12, 7, 9, 7]
    >>> pack(24, O)
    [8, 11, 23, 23, 24, 24]
    >>> O = [3, 16, 27, 23, 12, 7, 9, 10, 16, 23, 21, 13, 6, 20, 19, 11]
    >>> pack(40, O)
    [3, 19, 30, 39, 39, 39, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]
    """
    n = len(O)
    DP = [0 for e in O]

    dp0 = lambda x: O[0] if x >= O[0] else 0
    DP[0] = dp0(V)
    
    for i in range(1, n):
        v = V
        DP[i] = DP[i-1]
        for j in range(i, 0, -1):
            v = V-O[i]
            if dp0(v)+(V-v) >= DP[i]:
                DP[i] = dp0(v)+(V-v)
            for k in range(j-1, 0, -1):
                if v >= O[k]:
                    v -= O[k]
                    if dp0(v)+(V-v) >= DP[i]:
                        DP[i] = dp0(v)+(V-v)

    return DP

def rpack(V, O):
    """
    Recursion method.
    
    >>> O = [8, 3, 12, 7, 9, 7]
    >>> rpack(24, O)
    [8, 11, 23, 23, 24, 24]
    >>> O = [3, 16, 27, 23, 12, 7, 9, 10, 16, 23, 21, 13, 6, 20, 19, 11]
    >>> rpack(40, O)
    [3, 19, 30, 39, 39, 39, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]
    """
    n = len(O)
    DP = [0 for e in O]
    
    #@lru_cache
    def f(v, i = 0):
        if i == 0:
            if v >= O[i]:
                return O[i]
            else:
                return 0
        else:
            if v >= O[i]:
                return max(f(v, i-1), f(v-O[i], i-1)+O[i])
            else:
                return f(v, i-1)
    
    for i in range(n):
        DP[i] = f(V, i)
        
    return DP


def weight(A):
    """
    NOIP 1996.
    """
    pass

################################################################################

def numtri(A):
    """
    IOI94.
    
        7
       3 8
      8 1 0
     2 7 4 4
    4 5 2 6 5
    >>> A = [[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]
    >>> DP = numtri(A)
    >>> DP
    [[7], [10, 15], [18, 16, 15], [20, 25, 20, 19], [24, 30, 27, 26, 24]]
    >>> max(DP[-1])
    30
    """
    DP = [[i for i in e] for e in A]
    n = len(A)
    
    for i in range(1, n):
        m = len(A[i])
        for j in range(m):
            if j == 0:
                DP[i][j] = DP[i][j]+DP[i-1][0]
            elif j == m-1:
                DP[i][j] = DP[i][j]+DP[i-1][m-2]
            else:
                DP[i][j] = max(DP[i][j]+DP[i-1][j-1], DP[i][j]+DP[i-1][j])
    
    return DP


################################################################################

if __name__ == '__main__':
    import doctest
    doctest.testmod()

