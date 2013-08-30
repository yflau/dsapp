#! /usr/bin/env python
# coding: utf-8

import random
import Queue

################################################################################

def variance(a):
    """
    >>> a = [2, 5, 9, 4, 8, 7]
    >>> variance(a)
    5.805555555555556
    >>> b = [3, 4, 6, 7, 1, 1]
    >>> variance(b)
    5.222222222222222
    """
    n = len(a)
    mean = float(sum(a))/n
    variance = float(sum([pow((e-mean), 2) for e in a]))/n
    
    return variance

def impartition(A, p = None, r = None, di = 0, pivot = None):
    """
    Inplace randomized select element as pivot for multiple dimension array.
    
    >>> A = [(9,8), (3,0), (7,1), (2,5), (8,8), (5,2), (1,7), (0,3), (8,9)]
    >>> impartition(A, 0, 8, 0, 3)
    2
    >>> A
    [(1, 7), (0, 3), (2, 5), (7, 1), (8, 8), (5, 2), (9, 8), (3, 0), (8, 9)]
    >>> impartition(A, 0, 8, 1, 3)
    1
    >>> A
    [(3, 0), (7, 1), (2, 5), (0, 3), (8, 8), (5, 2), (9, 8), (1, 7), (8, 9)]
    """
    if p is None:
        p = 0
    if r is None:
        r = len(A)-1
    if pivot is None:
        pivot = random.randint(p, r)
    i = p
    x = A[pivot][di]
    for j in xrange(p, r+1):
        if j == pivot:
            continue
        if A[j][di] <= x:
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

def imqselect(a, di = 0, k = None, p = None, r = None):
    """
    Inplace quick select algorithm for multiple dimension array.
    
    >>> A = [(9,8), (3,0), (7,1), (2,5), (8,8), (5,2), (1,7), (0,3), (5,9)]
    >>> tmp = imqselect(A)
    >>> tmp[0][0]
    5
    >>> tmp[1]
    4
    >>> imqselect(A, 1)
    ((2, 5), 4)
    """
    n = len(a)
    if k is None:
        k = (n+1)/2
    if p is None:
        p = 0
    if r is None:
        r = n - 1
    pivot = impartition(a, p, r, di)+1
    n1 = pivot-p
    if k < n1:
        return imqselect(a, di, k, p, pivot-2)
    elif k > n1:
        return imqselect(a, di, k-n1, pivot, r)
    else:
        return a[pivot-1], pivot - 1

def median(a, di = 0):
    """
    Find the median of a and place the median at its position.
    
    @param di : dimension i for multiple dimension array.
    
    >>> A = [(9,8), (3,0), (7,1), (2,5), (8,8), (5,2), (1,7), (0,3), (5,9)]
    >>> a, m , i = median(A)
    >>> i
    5
    >>> A[i+1][0] > m[0]
    True
    >>> A = [(9,8), (3,0), (7,1), (2,5), (8,8), (5,2), (1,7), (0,3), (5,9)]
    >>> a, m , i = median(A, 1)
    >>> i
    4
    >>> A[i+1][1] > m[1]
    True
    """
    n = len(a)
    m, i = imqselect(a, di)
    
    for j in xrange(i+1, n):
        if a[j][di] == m[di]:
            i += 1
        else:
            break
    
    return a, m, i

################################################################################

class KDNode(object):
    
    def __init__(self, pt = None):
        self.data = pt
        self.split = 0
        self.left = None
        self.right = None
        self.parent = None

    def has_left(self):
        return self.left
    
    def has_right(self):
        return self.right

    def is_left(self):
        return self.parent and self.parent.left == self

    def is_right(self):
        return self.parent and self.parent.right == self

    def is_root(self):
        return not self.parent

    def is_leaf(self):
        return not (self.right or self.left)

    def has_any_children(self):
        return self.right or self.left

    def has_both_children(self):
        return self.right and self.left

    def __str__(self):
        return str(self.data)

    __repr__ = __str__


class KDTree(object):
    """
    >>> pts = [(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)]
    >>> kdt = KDTree(pts)
    >>> kdt.depth
    2
    >>> kdt.insert((3, 2))
    (5, 4)
    >>> kdt = KDTree(k = 2)
    >>> [kdt.insert(e) for e in [(5,4), (2,3), (9,6), (4,7), (8,1), (7,2)]]
    [(5, 4), (5, 4), (5, 4), (5, 4), (5, 4), (5, 4)]
    >>> kdt.depth
    3
    >>> kdt.min(0)
    (2, 3)
    >>> kdt.min(1)
    (8, 1)
    >>> kdt.pprint()
    """
    def __init__(self, pts = [], k = 3):
        if pts:
            self.k = len(pts[0])
        else:
            self.k = k
        self.depth = 0
        self.root = self.init(pts)

    def init(self, pts, depth = 0):
        if not pts:
            return 
        if depth > self.depth:
            self.depth = depth
        split = depth % self.k
        pts, m, i = median(pts, split)
        node = KDNode()
        node.data = m
        node.split = split
        node.left = self.init(pts[:i], depth+1)
        if node.left:
            node.left.parent = node
        node.right = self.init(pts[i+1:], depth+1)
        if node.right:
            node.right.parent = node
        
        return node

    def search(self, pt):
        return self._search(self.root, pt, 0)

    def _search(self, node, pt, depth = 0):
        split = depth % self.k
        if node.data == pt:
            return node
        elif pt[split] < node.data[split]:
            if node.has_left():
                return self._search(node.left, pt, depth+1)
            else:
                return None
        else:
            if node.has_right():
                return self._search(node.right, pt, depth+1)
            else:
                return None

    def balance(self):
        pass

    def insert(self, pt):
        if self.root:
            return self._insert(pt, self.root, 0)
        else:
            self.root = self._insert(pt, self.root, 0)
            return self.root

    def _insert(self, pt, node, depth = 0):
        if depth > self.depth:
            self.depth = depth
        split = depth % self.k
        if node is None:
            node = KDNode(pt)
            node.split = split
        elif node.data == pt:
            # how to handle duplicates?
            pass
        elif pt[split] < node.data[split]:
            node.left = self._insert(pt, node.left, depth+1)
            if node.left:
                node.left.parent = node
        else:
            node.right = self._insert(pt, node.right, depth+1)
            if node.right:
                node.right.parent = node
        
        return node

    def delete(self, pt):
        pass

    def min(self, split):
        return self._min(self.root, split, 0)

    def _min(self, node, split = 0, depth = 0):
        if not node:
            return None
        elif split == depth:
            if not node.has_left():
                return node.data
            else:
                return self._min(node.left, split, depth+1)
        else:
            lcmin = self._min(node.left, split, depth+1)
            rcmin = self._min(node.right, split, depth+1)
            opts = [e for e in [node.data, lcmin, rcmin] if e]
            
            return min(opts, key = lambda e: e[split])

    def succ(self, node):
        succ = None
        
        if node.has_right():
            succ = node.right.min()
        else:
            if node.parent:
                if node.is_left():
                    succ = node.parent
                else:
                    node.parent.right = None
                    succ = self.succ(node)
                    node.parent.right = node
                    
        return succ

    def nearest(self, k = 1):
        pass

    def preorder(self):
        return self._preorder(self.root)
    
    def _preorder(self, node):
        nodes = []
        nodes.append(node)
        if node.has_left():
            nodes.extend(self._preorder(node.left))
        if node.has_right():
            nodes.extend(self._preorder(node.right))
        
        return nodes

    def inorder(self):
        return self._inorder(self.root)
    
    def _inorder(self, node):
        nodes = []
        if node.has_left():
            nodes.extend(self._inorder(node.left))
        nodes.append(node)
        if node.has_right():
            nodes.extend(self._inorder(node.right))
        
        return nodes

    def postorder(self):
        return self._postorder(self.root)
    
    def _postorder(self, node):
        nodes = []
        if node.has_left():
            nodes.extend(self._postorder(node.left))
        if node.has_right():
            nodes.extend(self._postorder(node.right))
        nodes.append(node)
        
        return nodes

    def bft(self, node, level = 1):
        """Breadth first traversal."""
        q = Queue.Queue()
        level = level
        q.put((level, node))

        while not q.empty():
            level, node = q.get()
            yield (level, node)
            if node.has_left():
                q.put((level+1, node.left))
            if node.has_right():
                q.put((level+1, node.right))

    def levels(self):
        leveldict = {}

        for level, node in self.bft(self.root):
            leveldict.setdefault(level, []).append(node)

        return leveldict

    def pprint(self):
        nodes = self.inorder()
        length = [len(str(e)) for e in nodes]
        leveldict = self.levels()
        levels = leveldict.keys()
        for level in levels:
            levelnodes = leveldict.get(level)
            starts = []
            ends = []
            branches = []
            for node in levelnodes:
                index = nodes.index(node)
                start = sum([len(str(e)) for e in nodes[:index]])
                end = start + len(str(node))
                starts.append(start)
                ends.append(end)
                if node.is_left():
                    branches.append((end-1, '/'))
                elif node.is_right():
                    branches.append((start-1, '\\'))
                else:
                    if level > 1:
                        print 'error node: ', node
            if level > 1:
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
