#! /usr/bin/env python
# coding: utf-8

"""
Greedy algorithm.

Reference:
    
- Introduction to Algorithms.

"""

import heapq

INF = float('inf')


################################################################################

### activity selector problem

def dp_activity_selector(S, F):
    """
    Activity selector problem with dynamic programming method, maybe it's 
    different from the method of the book.
    
    f(0) = 1
    f(1) = max(f(0), f(0)+1)   if 0 is compatible with 1
           max(f(0))           if 1 is not compatibl with 2
    f(i) = max(f(i-1), f(j)+1) with 0 <= j < i, and j is compatible with i
    
    f(i) stands for the max compatible number of the first i activities.
    
    Notice: The recursive formula established based on the F is sorted 
    in ascending order, for if i is compatible with j, then i is compatible with
    all 0 <= k < j activities.
    
    >>> S = [1, 3, 0, 5, 3, 5,  6,  8,  8,  2, 12]
    >>> F = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    >>> DP, R = dp_activity_selector(S, F)
    >>> DP
    [1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4]
    >>> R
    [(1, 4), (5, 7), (8, 11), (12, 14)]
    >>> max(DP)
    4
    >>> len(R)
    4
    >>> S = [ 6, 8,  0, 12, 3, 5, 1, 3,  8,  2, 5]
    >>> F = [10, 11, 6, 14, 8, 9, 4, 5, 12, 13, 7]
    >>> DP, R = dp_activity_selector(S, F)
    >>> R
    [(1, 4), (5, 7), (8, 11), (12, 14)]
    """
    S, F = zip(*sorted(zip(S, F), key=lambda e:e[1]))   # ensure F in ascending order
    
    n = len(S)
    DP = [1 for i in range(n)]
    R = [(S[0], F[0])]
    
    for i in range(1, n):
        DP[i] = max(DP[:i])
        for j in range(i):
            if F[j] <= S[i] and DP[j] + 1 > DP[i]:
                DP[i] = DP[j] + 1
                R.append((S[i], F[i]))
    
    return DP, R

def recursive_activity_selector(S, F, L, i = 0, j = None):
    """
    >>> S = [1, 3, 0, 5, 3, 5,  6,  8,  8,  2, 12]
    >>> F = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    >>> recursive_activity_selector(S, F, len(S))
    [(1, 4), (5, 7), (8, 11), (12, 14)]
    >>> S = [1, 3, 0, 5, 3, 5,  6,  8,  8,  2, 12]
    >>> F = [8, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    >>> recursive_activity_selector(S, F, len(S))
    [(3, 5), (5, 7), (8, 11), (12, 14)]
    """
    if j is None:
        j = len(S)
    
    R = []
    if j-i == L:
        S, F = zip(*sorted(zip(S, F), key=lambda e:e[1]))
        R.append((S[0], F[0]))
        
    m = i+1
    while m < j and S[m] < F[i]:
        m += 1
        
    if m < j:
        R.append((S[m], F[m]))
        R.extend(recursive_activity_selector(S, F, L, m, j))
        return R
    else:
        return R

def greedy_activity_selector(S, F):
    """
    >>> S = [1, 3, 0, 5, 3, 5,  6,  8,  8,  2, 12]
    >>> F = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    >>> greedy_activity_selector(S, F)
    [(1, 4), (5, 7), (8, 11), (12, 14)]
    >>> S = [1, 3, 0, 5, 3, 5,  6,  8,  8,  2, 12]
    >>> F = [8, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    >>> greedy_activity_selector(S, F)
    [(3, 5), (5, 7), (8, 11), (12, 14)]
    """
    S, F = zip(*sorted(zip(S, F), key=lambda e:e[1]))
    
    n = len(S)
    R = [(S[0], F[0])]
    i = 0
    
    for m in range(1, n):
        if S[m] >= F[i]:
            R.append((S[m], F[m]))
            i = m
    
    return R

################################################################################

### Huffman coding

class Node(object):
    
    def __init__(self, key, value = '-'):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        return '(%s,%s)' % (self.key, self.value)
        
    __repr__ = __str__

    def is_leaf(self):
        return not (self.left and self.right)

    def is_left(self):
        return self.parent and self.parent.left == self

    def is_right(self):
        return self.parent and self.parent.right == self

    def inorder(self):
        nodes = []
        if self.left:
            nodes.extend(self.left.inorder())
        nodes.append(self)
        if self.right:
            nodes.extend(self.right.inorder())
            
        return nodes

    def encode(self):
        if not self.is_leaf():
            return {}
            
        code = []
        value = self.value
        
        while self.parent:
            if self.is_left():
                code.append(0)
            elif self.is_right():
                code.append(1)
            self = self.parent
        
        code.reverse()
        
        return {value: ''.join([str(e) for e in code])}

    def encode_table(self):
        nodes = self.inorder()
        table = {}
        
        for e in nodes:
            if e.is_leaf():
                table.update(e.encode())
        
        return table


def Huffman(C):
    """
    Construct a Humffman tree.
    
    >>> C = [(45,'a'), (13,'b'), (12,'c'), (16,'d'), (9,'e'), (5,'f')]
    >>> root = Huffman(C)
    >>> root.encode_table()
    {'a': '0', 'c': '100', 'b': '101', 'e': '1101', 'd': '111', 'f': '1100'}
    """
    n = len(C)
    Q = [(k, Node(k, v)) for k,v in C]
    heapq.heapify(Q)
    root = None

    for i in range(n-1):
        x = heapq.heappop(Q)[1]
        y = heapq.heappop(Q)[1]
        node = Node(x.key+y.key)
        node.left = x
        node.right = y
        x.parent = node
        y.parent = node
        heapq.heappush(Q, (node.key, node))
        if i == n-2:
            root = node
    
    return root

def huffman_encode(T, s):
    """
    Encode a string s with Huffman table T.
    
    >>> T = {'a': '0', 'c': '100', 'b': '101', 'e': '1101', 'd': '111', 'f': '1100'}
    >>> s = 'acdbfecadebcef'
    >>> huffman_encode(T, s)
    '0100111101110011011000111110110110011011100'
    """
    return ''.join([T.get(e) for e in s])

def huffman_decode(T, s):
    """
    Decode a string s with Huffman table T.
    
    >>> T = {'a': '0', 'c': '100', 'b': '101', 'e': '1101', 'd': '111', 'f': '1100'}
    >>> s = '0100111101110011011000111110110110011011100'
    >>> huffman_decode(T, s)
    'acdbfecadebcef'
    """
    result = []
    T = {v:k for k, v in T.items()}
    n = len(s)
    j = 0

    for i in range(1, n+1):
        if s[j:i] in T:
            result.append(T.get(s[j:i]))
            j = i
    
    return ''.join(result)

################################################################################

def delnum(I, k):
    """
    Delete number problem, choose high bit first.
    
    >>> I = 5934625578
    >>> delnum(I, 6)
    2557
    >>> I = '2358984379837'
    >>> delnum(I, 8)
    23337
    """
    R = []
    A = list(str(I))
    n = len(A)
    s = 0
    e = s + k + 1
    for j in range(n-k):
        im, vm = min([(i, v) for i,v in enumerate(A[s:e])], key=lambda t:t[1])
        R.append(vm)
        s += im+1
        e += 1
        
    return int(''.join(R))


################################################################################

if __name__ == '__main__':
    import doctest
    doctest.testmod()
