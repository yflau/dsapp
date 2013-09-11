#! /usr/bin/env python
# coding: utf-8

"""
Binomial heap.

Reference:

- Introduction to Algorithms.

"""

import Queue

INF = float('inf')


class BinomialNode(object):

    def __init__(self, key, value = None):
        self.key = key
        self.value = value
        self.degree = 0
        self.child = None
        self.parent = None
        self.sibling = None

    def link_parent(self, node):
        self.parent = node
        self.sibling = node.child
        node.child = self
        node.degree += 1

        return self

    def link_son(self, node):
        node.parent = self
        node.sibling = self.child
        self.child = node
        self.degree += 1

        return self

    def __str__(self):
        return '(%s)->' % self.key if self.sibling else '(%s)' % self.key

    __repr__ = __str__

    def nrow(self):
        """the number of rows of the binomial tree."""
        return self.degree + 1

    def ncol(self):
        """the number of columns of the binomial tree."""
        return pow(2, self.degree-1) if self.degree > 1 else 1

    def bft(self, level = 0):
        """Breadth first traversal."""
        q = Queue.Queue()

        if not self:
            yield self

        icol = self.ncol() - 1
        q.put((level, icol, self))

        while not q.empty():
            level, icol, node = q.get()
            yield (level, icol, node)
            child = node.child
            if child:
                if node.degree > 1:
                    icol = icol - child.ncol()
                q.put((level+1, icol, child))
                while child.sibling:
                    icol += child.sibling.ncol()
                    q.put((level+1, icol, child.sibling))
                    child = child.sibling

    def pprint(self, colwidth = 6):
        """
        >>> kvs = [(10,)]
        >>> node = binomial_tree(kvs)
        >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
        (10)
        >>> kvs = [(1,), (25,)]
        >>> node = binomial_tree(kvs)
        >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
         (1)
        (25)
        >>> kvs = [(1,), (25,), (12,), (18,)]
        >>> node = binomial_tree(kvs)
        >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
              (1)
        (12)->(25)
        (18)
        >>> kvs = [(6,), (29,), (14,), (38,), (8,), (17,), (11,), (27,)]
        >>> node = binomial_tree(kvs)
        >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
                          (6)
              (8)-> (14)->(29)
        (11)->(17)  (38)
        (27)
        >>> kvs = [
        ...     (6,), (44,), (10,), (17,), (29,), (31,), (48,), (50,),
        ...     (8,), (22,), (23,), (24,), (30,), (32,), (45,), (55,)
        ... ]
        >>> node = binomial_tree(kvs)
        >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
                                                  (6)
                          (8)->       (29)->(10)->(44)
              (30)->(23)->(22)  (48)->(31)  (17)
        (45)->(32)  (24)        (50)
        (55)
        """
        r = []
        d = {}
        ncol = self.ncol()
        nrow = self.nrow()
        width = ncol * colwidth

        for irow, icol, node in self.bft():
            d.setdefault(irow, {}).update({icol : node})

        for i in range(nrow):
            tmp = [str(d[i].get(j, '')).ljust(colwidth) for j in range(ncol)]
            r.append(''.join(tmp).rjust(width))

        return '\n'.join(r)


def binomial_tree(kvs = []):
    """
    Construct a Binomial tree from a list of k,v pairs.

    >>> kvs = [(10,)]
    >>> node = binomial_tree(kvs)
    >>> list(node.bft())
    [(0, 0, (10))]
    >>> kvs = [(1,), (25,)]
    >>> node = binomial_tree(kvs)
    >>> list(node.bft())
    [(0, 0, (1)), (1, 0, (25))]
    >>> kvs = [(1,), (25,), (12,), (18,)]
    >>> node = binomial_tree(kvs)
    >>> list(node.bft())
    [(0, 1, (1)), (1, 0, (12)->), (1, 1, (25)), (2, 0, (18))]
    >>> kvs = [(6,), (29,), (14,), (38,), (8,), (17,), (11,), (27,)]
    >>> node = binomial_tree(kvs)
    >>> list(node.bft())
    [(0, 3, (6)), (1, 1, (8)->), (1, 2, (14)->), (1, 3, (29)), (2, 0, (11)->), (2, 1, (17)), (2, 2, (38)), (3, 0, (27))]
    """
    n = len(kvs)
    if n == 0:
        return None
    elif n == 1:
        return BinomialNode(*kvs[0])
    elif n == 2:
        return BinomialNode(*kvs[0]).link_son(BinomialNode(*kvs[1]))
    elif n%2 == 0:
        m = n/2
        n1 = binomial_tree(kvs[:m])
        n2 = binomial_tree(kvs[m:])
        return n1.link_son(n2)
    else:
        pass



class BinomialHeap(object):

    def __init__(self, head = None):
        """
        >>> head = BinomialNode(10)
        >>> bh = BinomialHeap(head)
        >>> kvs = [(1,), (25,), (12,), (18,)]
        >>> n1 = binomial_tree(kvs)
        >>> kvs = [(6,), (29,), (14,), (38,), (8,), (17,), (11,), (27,)]
        >>> n2 = binomial_tree(kvs)
        >>> head.sibling = n1
        >>> n1.sibling = n2
        >>> list(bh.bft()) # doctest: +ELLIPSIS
        [(0, 0, (10)->), (0, 2, (1)->), ..., (3, 3, (27))]
        >>> print bh.pprint() # doctest: +NORMALIZE_WHITESPACE
        (10)->      (1)->                   (6)
              (12)->(25)        (8)-> (14)->(29)
              (18)        (11)->(17)  (38)
                          (27)
        >>> bh.minimum()
        (1)->
        """
        self.head = head

    def build(self, treelist = []):
        """
        Build a binomial heap from a list of binomial tree, each of which contains
        a list of kv pairs.
        
        >>> bh = BinomialHeap()
        >>> bh.build([
        ...     [(10,)], 
        ...     [(1,), (25,), (12,), (18,)], 
        ...     [(6,), (29,), (14,), (38,), (8,), (17,), (11,), (27,)]
        ... ])
        >>> print bh.pprint() # doctest: +NORMALIZE_WHITESPACE
        (10)->      (1)->                   (6)
              (12)->(25)        (8)-> (14)->(29)
              (18)        (11)->(17)  (38)
                          (27)
        """
        if len(treelist) == 0:
            return self
        elif len(treelist[0]) != 1:
            return self
        else:
            treelist = [binomial_tree(e) for e in treelist]
            n = len(treelist) - 1
            for i in range(n):
                treelist[i].sibling = treelist[i+1]
            if n > 1:
                self.head = treelist[0]

    def minimum(self):
        """
        >>> H1 = BinomialHeap()
        >>> H1.build([
        ...     [(12,)], 
        ...     [(7,), (25,)], 
        ...     [(3,), (33,), (28,), (41,)]
        ... ])
        >>> H1.minimum()
        (3)
        """
        y = None
        x = self.head
        min = INF

        while x:
            if x.key < min:
                min = x.key
                y = x
            x = x.sibling

        return y

    def insert(self, node):
        node.parent = None
        node.child = None
        node.sibling = None
        node.degree = 0
        H = BinomialHeap(node)
        
        return union(self, H)

    def pop(self):
        """
        Extract min.
        
        >>> H1 = BinomialHeap()
        >>> H1.build([
        ...     [(12,)], 
        ...     [(7,), (25,)], 
        ...     [(3,), (33,), (28,), (41,)]
        ... ])
        >>> print H1.pprint() # doctest: +NORMALIZE_WHITESPACE
        (12)->(7)->       (3)
              (25)  (28)->(33)
                    (41)
        >>> H = H1.pop()
        >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
        (12)->      (7)
        (33)  (28)->(25)
              (41)
        """
        # find prev and minimum
        x = self.head
        prev = self.head
        minimum = self.head
        minkey = x.key

        while x:
            if x.sibling:
                if x.sibling.key < minkey:
                    minkey = x.sibling.key
                    prev = x
                    minimum = x.sibling
            x = x.sibling

        # delete minimum
        prev.sibling = minimum.sibling
        
        # reverse the children of minimum and become a new binomial heap
        children = []
        x = minimum.child
        while x:
            children.append(x)
            x = x.sibling
        nchildren = len(children)
        for i in range(nchildren-1, 0, -1):
            children[i].sibling = children[i-1]
            children[i].parent = None
        children[0].parent = None
        children[0].sibling = None
        
        # union binoimal heaps
        H = BinomialHeap()
        H.head = children[-1]
        
        return union(self, H)

    def decrease_key(self, x, k):
        """
        >>> H1 = BinomialHeap()
        >>> H1.build([
        ...     [(12,)], 
        ...     [(7,), (25,)], 
        ...     [(3,), (33,), (28,), (41,)]
        ... ])
        >>> node = H1.head.sibling.sibling.child.child
        >>> print H1.pprint() # doctest: +NORMALIZE_WHITESPACE
        (12)->(7)->       (3)
              (25)  (28)->(33)
                    (41)
        >>> H1.decrease_key(node, 2)
        >>> print H1.pprint() # doctest: +NORMALIZE_WHITESPACE
        (12)->(7)->       (2)
              (25)  (3)-> (33)
                    (28)
        """
        if k > x.key:
            print 'new key is greater than current'
            return
        x.key = k
        y = x
        z = y.parent
        while z != None and y.key < z.key:
            tmp = y.key
            y.key = z.key
            z.key = tmp
            # exchange satellite data
            y = z
            z = y.parent

    def delete(self, node):
        """
        >>> H1 = BinomialHeap()
        >>> H1.build([
        ...     [(12,)], 
        ...     [(7,), (25,)], 
        ...     [(3,), (33,), (28,), (41,)]
        ... ])
        >>> node = H1.head.sibling.sibling.child.child
        >>> print H1.pprint() # doctest: +NORMALIZE_WHITESPACE
        (12)->(7)->       (3)
              (25)  (28)->(33)
                    (41)
        >>> H1.delete(node)
        >>> print H1.pprint() # doctest: +NORMALIZE_WHITESPACE
        (12)->      (3)
        (33)  (7)-> (28)
              (25)
        """
        self.decrease_key(node, -INF)
        self.pop()

    def merge(self, H):
        pass
        
    def union(self, H):
        pass

    def nrow(self):
        nrow = 0
        p = self.head

        while p:
            nrow = p.nrow()
            p = p.sibling

        return nrow

    def ncol(self):
        ncol = 0
        p = self.head
        while p:
            ncol += p.ncol()
            p = p.sibling

        return ncol

    def bft(self, level = 0):
        """Breadth first traversal."""
        q = Queue.Queue()

        if not self.head:
            yield self.head

        p = self.head
        icol = p.ncol() - 1

        while p:
            q.put((level, icol, p))
            p = p.sibling
            if p:
                icol += p.ncol()

        while not q.empty():
            level, icol, node = q.get()
            yield (level, icol, node)
            child = node.child
            if child:
                if node.degree > 1:
                    icol = icol - child.ncol()
                q.put((level+1, icol, child))
                while child.sibling:
                    icol += child.sibling.ncol()
                    q.put((level+1, icol, child.sibling))
                    child = child.sibling

    def pprint(self, colwidth = 6):
        r = []
        d = {}
        ncol = self.ncol()
        nrow = self.nrow()
        width = ncol * colwidth

        for irow, icol, node in self.bft():
            d.setdefault(irow, {}).update({icol : node})

        for i in range(nrow):
            tmp = [str(d[i].get(j, '')).ljust(colwidth) for j in range(ncol)]
            r.append(''.join(tmp).rjust(width))

        return '\n'.join(r)

def link(y, z):
    y.parent = z
    y.sibling = z.child
    z.child = y
    z.degree += 1

def merge(H1, H2):
    """
    Merge sort.
    
    >>> H1 = BinomialHeap()
    >>> H1.build([
    ...     [(12,)], 
    ...     [(7,), (25,)], 
    ...     [(15,), (33,), (28,), (41,)]
    ... ])
    >>> print H1.pprint() # doctest: +NORMALIZE_WHITESPACE
    (12)->(7)->       (15)
          (25)  (28)->(33)
                (41)
    >>> H2 = BinomialHeap()
    >>> H2.build([
    ...     [(18,)], 
    ...     [(3,), (37,)], 
    ...     [
    ...         (6,), (44,), (10,), (17,), (29,), (31,), (48,), (50,),
    ...         (8,), (22,), (23,), (24,), (30,), (32,), (45,), (55,)
    ...     
    ...     ]
    ... ])
    >>> print H2.pprint() # doctest: +NORMALIZE_WHITESPACE
    (18)->(3)->                                           (6)
          (37)                    (8)->       (29)->(10)->(44)
                      (30)->(23)->(22)  (48)->(31)  (17)
                (45)->(32)  (24)        (50)
                (55)
    >>> H = merge(H1, H2)
    >>> print H.pprint()  # doctest: +NORMALIZE_WHITESPACE
    (12)->(18)->(7)-> (3)->       (15)->                                          (6)
                (25)  (37)  (28)->(33)                    (8)->       (29)->(10)->(44)
                            (41)              (30)->(23)->(22)  (48)->(31)  (17)
                                        (45)->(32)  (24)        (50)
                                        (55)
    """
    H = BinomialHeap()

    h1 = H1.head
    h2 = H2.head

    if h1.degree <= h2.degree:
        H.head = h1
        h1 = h1.sibling
    else:
        H.head = h2
        h2 = h2.sibling

    h = H.head

    while h1 and h2:
        if h1.degree <= h2.degree:
            h.sibling = h1
            h1 = h1.sibling
        else:
            h.sibling = h2
            h2 = h2.sibling
        h = h.sibling
        if not h1:
            h.sibling = h2
            break
        if not h2:
            h.sibling = h1
            break

    return H

def union(H1, H2):
    """
    Union two binomial heaps.
    
    >>> H1 = BinomialHeap()
    >>> H1.build([
    ...     [(12,)], 
    ...     [(7,), (25,)], 
    ...     [(15,), (33,), (28,), (41,)]
    ... ])
    >>> print H1.pprint() # doctest: +NORMALIZE_WHITESPACE
    (12)->(7)->       (15)
          (25)  (28)->(33)
                (41)
    >>> H2 = BinomialHeap()
    >>> H2.build([
    ...     [(18,)], 
    ...     [(3,), (37,)], 
    ...     [
    ...         (6,), (44,), (10,), (17,), (29,), (31,), (48,), (50,),
    ...         (8,), (22,), (23,), (24,), (30,), (32,), (45,), (55,)
    ...     
    ...     ]
    ... ])
    >>> print H2.pprint() # doctest: +NORMALIZE_WHITESPACE
    (18)->(3)->                                           (6)
          (37)                    (8)->       (29)->(10)->(44)
                      (30)->(23)->(22)  (48)->(31)  (17)
                (45)->(32)  (24)        (50)
                (55)
    >>> H = union(H1, H2)
    >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
    (12)->                  (3)->                                           (6)
    (18)        (15)->(7)-> (37)                    (8)->       (29)->(10)->(44)
          (28)->(33)  (25)              (30)->(23)->(22)  (48)->(31)  (17)
          (41)                    (45)->(32)  (24)        (50)
                                  (55)
    """
    H = merge(H1, H2)

    if H.head is None:
        return H

    prevx = None
    x = H.head
    nextx = x.sibling

    while nextx:
        if (x.degree != nextx.degree) or \
           (nextx.sibling and nextx.sibling.degree == x.degree):
            prevx = x
            x = nextx
        elif x.key <= nextx.key:
            x.sibling = nextx.sibling
            x.link_son(nextx)
        else:
            if prevx is None:
                H.head = nextx
            else:
                prevx.sibling = nextx
            x.link_parent(nextx)
            x = nextx

        nextx = x.sibling

    return H


if __name__ == '__main__':
    import doctest
    doctest.testmod()

