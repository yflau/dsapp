#! /usr/bin/env python
# coding: utf-8

"""
Max-heap implemention.

Reference:

- Introduction to Algorithms.
- http://cs.anu.edu.au/~Alistair.Rendell/Teaching/apac_comp3600/

"""

def max_heapify(A, i, heap_size = None):
    """
    >>> A = [1, 3, 6, 0, 2, 4, 5]
    >>> max_heapify(A, 0)
    >>> A
    [6, 3, 5, 0, 2, 4, 1]
    """
    if heap_size is None:
        heap_size = len(A)
    l = 2*i+1
    r = 2*i+2
    if l < heap_size and A[l] > A[i]:
        largest = l
    else:
        largest = i
    if r < heap_size and A[r] > A[largest]:
        largest = r
    if largest != i:
        tmp = A[i]
        A[i] = A[largest]
        A[largest] = tmp
        max_heapify(A, largest, heap_size)

def build_max_heap(A):
    """
    >>> A = [1, 2, 3, 4, 9, 8, 7, 10, 16, 14]
    >>> build_max_heap(A)
    >>> A
    [16, 14, 8, 10, 9, 3, 7, 2, 4, 1]
    """
    heap_size = len(A)
    for i in xrange(heap_size/2, -1, -1):
        max_heapify(A, i, heap_size)

def heapsort(A):
    """
    >>> A = [1, 2, 3, 4, 9, 8, 7, 10, 16, 14]
    >>> heapsort(A)
    >>> A
    [1, 2, 3, 4, 7, 8, 9, 10, 14, 16]
    """
    heap_size = len(A)
    build_max_heap(A)
    for i in xrange(heap_size-1, 0, -1):
        tmp = A[0]
        A[0] = A[i]
        A[i] = tmp
        heap_size -= 1
        max_heapify(A, 0, heap_size)

def heap_maximum(A):
    return A[0]

def heap_extract_max(A):
    """
    heappop.
    
    >>> A = [16, 14, 8, 10, 9, 3, 7, 2, 4, 1]
    >>> heap_extract_max(A)
    16
    >>> A
    [14, 10, 8, 4, 9, 3, 7, 2, 1]
    """
    heap_size = len(A)
    if heap_size < 0:
        print 'heap underflow'
    max = A[0]
    A[0] = A.pop(heap_size-1)
    heap_size -= 1
    max_heapify(A, 0, heap_size)
    
    return max

def heap_increase_key(A, i, key):
    """
    >>> A = [16, 14, 8, 10, 9, 3, 7, 2, 4, 1]
    >>> heap_increase_key(A, 9, 15)
    >>> A
    [16, 15, 8, 10, 14, 3, 7, 2, 4, 9]
    """
    if key < A[i]:
        print 'new key is smaller than current key'
    A[i] = key
    while i > 0 and A[(i-1)/2] < A[i]:
        tmp = A[i]
        A[i] = A[(i-1)/2]
        A[(i-1)/2] = tmp
        i = (i-1)/2

def max_heap_insert(A, key):
    """
    >>> A = [16, 14, 8, 10, 9, 3, 7, 2, 4, 1]
    >>> max_heap_insert(A, 18)
    >>> A
    [18, 16, 8, 10, 14, 3, 7, 2, 4, 1, 9]
    """
    A.append(float('-inf'))
    heap_increase_key(A, len(A)-1, key)

################################################################################

from collections import deque
from math import log

def heap_inorder(A, i = 0, heap_size = None):
    """
    Iterate a heap inorder.
    
    >>> A = [16, 14, 8, 10, 9, 3, 7, 2, 4, 1]
    >>> list(heap_inorder(A))
    [2, 10, 4, 14, 1, 9, 16, 3, 8, 7]
    """
    result = deque()
    if heap_size is None:
        heap_size = len(A)
    if i >= heap_size:
        return []
    if 0 <= i < heap_size:
        result.append(A[i])
    left = heap_inorder(A, 2*i+1, heap_size)
    left.reverse()
    result.extendleft(left)
    result.extend(heap_inorder(A, 2*i+2, heap_size))
    
    return result

def heap_pprint(A):
    """
    Print a heap as a binary tree.
    
    >>> A = [16, 14, 8, 10, 9, 3, 7, 2, 4, 1]
    >>> heap_pprint(A) # doctest: +SKIP
            16
         /    \
        14     8
      /   \   /\
     10    9  3 7
    / \   /
    2  4  1
    """
    nodes = list(heap_inorder(A))
    length = [len(str(e)) for e in nodes]
    levels = int(log(len(A) + 1, 2))
    for level in range(levels + 1):
        levelnodes = A[pow(2, level)-1 : pow(2, level+1)-1]
        starts = []
        ends = []
        branches = []
        for node in levelnodes:
            oindex = A.index(node)
            index = nodes.index(node)
            start = sum([len(str(e)) for e in nodes[:index]])
            end = start + len(str(node))
            starts.append(start)
            ends.append(end)
            if oindex == 0:
                if level > 0:
                    print 'error node: ', node
            if oindex % 2 == 1:
                branches.append((end-1, '/'))
            elif oindex % 2 == 0:
                branches.append((start-1, '\\'))
            else:
                pass
        if level > 0:
            spaces = [branches[0][0]]
            spaces.extend([branches[k+1][0] - branches[k][0] - 1 for k in range(len(branches)-1)])
            pair = ['%s%s' % (' '*spaces[m], branches[m][1]) for m in range(len(branches))]
            print ''.join(pair)
        spaces = [starts[0]]
        spaces.extend([starts[i] - ends[i-1] for i in range(1, len(starts))])
        pair = ['%s%s' % (' '*spaces[j], levelnodes[j]) for j in range(len(spaces))]
        print ''.join(pair)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
