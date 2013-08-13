#! /usr/bin/env python
# coding: utf-8

import sys

def lcs(a, b):
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
    n = len(r) - 1
    C = [[0 for i in range(n)] for i in range(n)]
    for d in range(1, n):
        for i in range(n-d):
            j = i + d
            C[i][j] = sys.maxint
            for k in (i+1, j):
                if C[i][j] > C[i][k-1]+C[k][j]+r[i]*r[k]*r[j+1]:
                    print i,j,k,C[i][k-1],C[k][j]+r[i],r[i]*r[k]*r[j+1]
                C[i][j] = min(C[i][j], C[i][k-1]+C[k][j]+r[i]*r[k]*r[j+1])

    return C

if __name__ == '__main__':
    from pprint import pprint
    #pprint(lcs('xyxxzxyzxy', 'zxzyyzxxyxxz'))
    pprint(matchain([5, 10, 4, 6, 10, 2]))

