#! /usr/bin/env python
# coding: utf-8

"""
K-Dimnsion Tree.

Reference:

- http://en.wikipedia.org/wiki/K-d_tree
- http://www.cs.umd.edu/class/spring2002/cmsc420-0401/pbasic.pdf
- http://www.cs.fsu.edu/~lifeifei/cis5930/kdtree.pdf
- http://underthehood.blog.51cto.com/2531780/687160
- http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.28.6468&rep=rep1&type=pdf
"""

import random
import Queue
from heapq import heappush, heappop, heappushpop

INF = float('inf')

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

def distance(pt1, pt2):
    """
    >>> pow(distance((2.1, 3.1), (8, 1)), 0.5)
    6.26258732474047
    """
    k = len(pt1)
    return sum([pow((pt1[i]-pt2[i]), 2) for i in range(k)])

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
    if p is None:
        p = 0
    if r is None:
        r = n - 1
    if k is None:
        k = (r-p+2)/2
    pivot = impartition(a, p, r, di)+1
    n1 = pivot-p
    if k < n1:
        return imqselect(a, di, k, p, pivot-2)
    elif k > n1:
        return imqselect(a, di, k-n1, pivot, r)
    else:
        return a[pivot-1], pivot - 1

def median(a, di = 0, p = None, r = None):
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
    >>> A = [(2,3), (5,4), (2, 3), (9,6), (4,7), (8,1), (7,2)]
    >>> a, m, i = median(A, 0, 0, 3)
    """
    n = len(a)
    if p is None:
        p = 0
    if r is None:
        r = n - 1
    m, i = imqselect(a, di, p = p, r = r)

    for j in xrange(i+1, r+1):
        if a[j][di] == m[di]:
            i += 1
        else:
            break

    return a, m, i

def median_with_sort(a, di = 0):
    n = len(a)
    a = sorted(a, key=lambda e: e[di])
    i = n/2
    m = a[i]

    for j in xrange(i+1, n):
        if a[j][di] == m[di]:
            i += 1
        else:
            break

    return a, m, i

################################################################################


class KDNode(object):

    def __init__(self, pt = None, split = 0):
        self.data = pt
        self.split = split
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

    @property
    def depth(self):
        """depth of node, root is 0."""
        depth = 0
        parent = self.parent

        while parent is not None:
            depth += 1
            parent = parent.parent

        return depth

    def __str__(self):
        return str(self.data)

    __repr__ = __str__


class KDTree(object):
    """
    >>> pts = [(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)]
    >>> kdt = KDTree(pts)
    >>> kdt.pprint()  # doctest: +SKIP
                (5, 4)
         /                 \
    (2, 3)                  (7, 2)
         \                 /     \
          (4, 7)      (8, 1)      (9, 6)
    >>> node = kdt.search((2, 3))
    >>> node.parent
    (5, 4)
    >>> node.depth
    1
    >>> node.parent.parent
    >>> kdt.depth
    2
    >>> kdt.insert((3, 2))
    (5, 4)
    >>> kdt = KDTree(k = 2)
    >>> [kdt.insert(e) for e in [(5,4), (2,3), (9,6), (4,7), (8,1), (7,2)]]
    [(5, 4), (5, 4), (5, 4), (5, 4), (5, 4), (5, 4)]
    >>> kdt.depth
    3
    >>> kdt.min(kdt.root, 0)
    (2, 3)
    >>> kdt.min(kdt.root, 1)
    (8, 1)
    >>> kdt.max(kdt.root, 0)
    (9, 6)
    >>> kdt.max(kdt.root, 1)
    (4, 7)
    >>> kdt.max(kdt.root.right, 1)
    (9, 6)
    >>> node = kdt.search((2, 3))
    >>> node
    (2, 3)
    >>> node.parent
    (5, 4)
    >>> node.parent.parent
    >>> kdt.search((3, 8))
    >>> kdt.delete(kdt.root, (5, 4))
    (7, 2)
    """
    def __init__(self, pts = [], k = 3):
        if pts:
            self.k = len(pts[0])
        else:
            self.k = k
        self.depth = 0
        self.root = self.init(pts)
        #self.root = self.init_inplace(pts)

    def init(self, pts, depth = 0):
        if not pts:
            return
        if depth > self.depth:
            self.depth = depth
        split = depth % self.k
        pts, m, i = median(pts, split)  # slower than sort, why?
        #pts, m, i = median_with_sort(pts, split)
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

    def init_inplace(self, pts, depth = 0, p = None, r = None):
        """Memory is also 260 MB, same as init method."""
        if not pts:
            return
        if depth > self.depth:
            self.depth = depth
        split = depth % self.k
        n = len(pts)
        if p is None:
            p = 0
        if r is None:
            r = n - 1
        pts, m, i = median(pts, split, p, r)
        node = KDNode()
        node.data = m
        node.split = split
        if p <= i-1:
            node.left = self.init_inplace(pts, depth+1, p, i-1)
            if node.left:
                node.left.parent = node
        if i+1 <= r:
            node.right = self.init_inplace(pts, depth+1, i+1, r)
            if node.right:
                node.right.parent = node

        return node

    def search(self, pt):
        return self._search(self.root, pt)

    def _search(self, node, pt):
        if node is None:
            return None
        nodesplit = node.split
        if node.data == pt:
            return node
        elif pt[nodesplit] < node.data[nodesplit]:
            if node.has_left():
                return self._search(node.left, pt)
            else:
                return None
        else:
            if node.has_right():
                return self._search(node.right, pt)
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

    def delete(self, node, pt):
        if node is None:
            return None
        split = node.split
        sonsplit = (split + 1) % self.k
        if pt[split] < node.data[split]:
            node.left = self.delete(node.left, pt)
        elif pt[split] > node.data[split]:
            node.right = self.delete(node.right, pt)
        else:
            if node.is_leaf():
                if node.is_left():
                    node.parent.left = None
                else:
                    node.parent.right = None
                return None
            elif node.has_right():
                succdata = self.min(node.right, node.split)
                node.data = succdata
                node.right = self.delete(node.right, succdata)
            else:
                prevdata = self.max(node.left, node.split)
                node.data = prevdata
                node.left = self.delete(node.left, prevdata)

        return node

    def min(self, node, split = 0):
        if not node:
            return None
        else:
            nodesplit = node.split
            if split == nodesplit:
                if not node.has_left():
                    return node.data
                else:
                    return self.min(node.left, split)
            else:
                lcmin = self.min(node.left, split)
                rcmin = self.min(node.right, split)
                opts = [e for e in [node.data, lcmin, rcmin] if e]

                return min(opts, key = lambda e: e[split])

    def max(self, node, split = 0):
        if not node:
            return None
        else:
            nodesplit = node.split
            if split == nodesplit:
                if not node.has_right():
                    return node.data
                else:
                    return self.max(node.right, split)
            else:
                lcmax = self.max(node.left, split)
                rcmax = self.max(node.right, split)
                opts = [e for e in [node.data, lcmax, rcmax] if e]

                return max(opts, key = lambda e: e[split])

    def nearest(self, pt, k = 1):
        """
        Recursive version of NN search.
        
        >>> kdt = KDTree(k = 2)
        >>> [kdt.insert(e) for e in [(7,2), (5,4), (2,3), (9,6), (4,7), (8,1)]]
        [(7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2)]
        >>> kdt.nearest((2.1, 3.1))
        [((2, 3), 0.14142135623730964)]
        >>> kdt.nearest((2, 4.5))
        [((2, 3), 1.5)]
        >>> kdt.pprint() # doctest: +SKIP
                          (7, 2)
                   /                 \
              (5, 4)                  (9, 6)
             /     \                 /
        (2, 3)      (4, 7)      (8, 1)
        """
        result = self._nearest(self.root, pt, k, [])
        result = [heappop(result) for i in range(len(result))][::-1]
        result = [(e[1], pow(abs(e[0]), 0.5)) for e in result]
        
        return result

    def _nearest(self, node, pt, k = 1, result = []):
        if node is None:
            return (None, float('inf'))
        
        data = node.data
        split = node.split
        dist = distance(data, pt)

        if node.is_leaf():
            if len(result) < k:
                heappush(result, (-dist, node))
            else:
                heappushpop(result, (-dist, node))
        else:
            if pt[split] <= data[split]:
                nearer = node.left
                further = node.right
            else:
                nearer = node.right
                further = node.left
    
            self._nearest(nearer, pt, k, result)
            if len(result) < k:
                heappush(result, (-dist, node))
            else:
                heappushpop(result, (-dist, node))
            dmax = -result[0][0] if result else INF
            if abs(pt[split]-data[split]) <= pow(dmax, 0.5):
                self._nearest(further, pt, k, result)
        
        return result

    def inearest(self, pt, k = 1):
        """
        Iteration version of NN search.
        
        >>> kdt = KDTree(k = 2)
        >>> [kdt.insert(e) for e in [(7,2), (5,4), (2,3), (9,6), (4,7), (8,1)]]
        [(7, 2), (7, 2), (7, 2), (7, 2), (7, 2), (7, 2)]
        >>> kdt.inearest((2.1, 3.1))
        [((2, 3), 0.14142135623730964)]
        >>> kdt.inearest((2, 4.5))
        [((2, 3), 1.5)]
        >>> kdt.pprint() # doctest: +SKIP
                          (7, 2)
                   /                 \
              (5, 4)                  (9, 6)
             /     \                 /
        (2, 3)      (4, 7)      (8, 1)
        """
        return self._inearest(self.root, pt, k)

    def _inearest(self, node, pt, k = 1):
        if node is None:
            return (None, float('inf'))
        result = []

        def generate_sp(node):
            sp = []
            while node:
                sp.append(node)
                data = node.data
                split = node.split
                if pt[split] <= data[split]:
                    node = node.left
                else:
                    node = node.right
            return sp
        
        sp = generate_sp(node)
        nearest = sp.pop(-1)
        dnearest = distance(nearest.data, pt)
        heappush(result, (-dnearest, nearest))

        # backtracking
        while sp:
            back = sp.pop(-1)
            data = back.data
            dback = distance(data, pt)
            if back.is_leaf():
                if len(result) < k:
                    heappush(result, (-dback, back))
                else:
                    if dback < -result[0][0]:
                        heappushpop(result, (-dback, back))
            else:
                split = back.split
                if len(result) < k:
                    heappush(result, (-dback, back))
                else:
                    heappushpop(result, (-dback, back))
                if abs(pt[split]-data[split]) <= pow(-result[0][0], 0.5):
                    if pt[split] <= data[split]:
                        sp.extend(generate_sp(back.right))
                    else:
                        sp.extend(generate_sp(back.left))

        result = [heappop(result) for i in range(len(result))][::-1]
        result = [(e[1], pow(abs(e[0]), 0.5)) for e in result]

        return result

    def search_range(self, pt, radius):
        """
        Find all points within distance radius of point(s) x.
        
        >>> kdt = KDTree(zip(range(10), range(10)))
        >>> kdt.search_range((1, 1), 2)
        [((0, 0), 1.4142135623730951), ((1, 1), 0.0), ((2, 2), 1.4142135623730951)]
        >>> kdt.pprint() # doctest: +SKIP
        """
        return self._search_range(self.root, pt, radius, [])

    def _search_range(self, node, pt, radius, result = []):
        if node is None:
            return (None, float('inf'))

        data = node.data
        split = node.split
        dist = distance(data, pt)

        if node.is_leaf():
            if pow(dist, 0.5) <= radius:
                result.append((node, pow(dist, 0.5)))
        else:
            if pt[split] <= data[split]:
                nearer = node.left
                further = node.right
            else:
                nearer = node.right
                further = node.left
            
            self._search_range(nearer, pt, radius, result)
            if pow(dist, 0.5) <= radius:
                result.append((node, pow(dist, 0.5)))
            if abs(pt[split]-data[split]) <= radius:
                self._search_range(further, pt, radius, result)
        
        return result

    #### some common methods

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

