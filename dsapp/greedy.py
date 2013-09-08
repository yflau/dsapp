#! /usr/bin/env python
# coding: utf-8

"""
Greedy algorithm.

Referenc:
    
- Introduction to Algorithms.

"""

import heapq


################################################################################

def activity_selector_dp(S, F):
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
    >>> DP = activity_selector_dp(S, F)
    >>> DP
    [1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4]
    >>> max(DP)
    4
    """
    n = len(S)
    DP = [1 for i in range(n)]
    
    for i in range(1, n):
        DP[i] = max(DP[:i])
        for j in range(i):
            if F[j] <= S[i]:
                if DP[j] + 1 > DP[i]:
                    DP[i] = DP[j] + 1
    
    return DP

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


if __name__ == '__main__':
    import doctest
    doctest.testmod()

