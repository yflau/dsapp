#! /usr/bin/env python
# coding: utf-8

"""
Fibonacci heap.

Reference:

- Introduction to Algorithms.

"""

import Queue
import math
import heapq

INF = float('inf')


class FibonacciNode(object):

    def __init__(self, key, value = None):
        self.key = key
        self.value = value
        self.degree = 0
        self.child = None
        self.parent = None
        self.left = self
        self.right = self
        self.mark = False

    def link_son(self, son):
        # remove son
        son.left.right = son.right
        son.right.left = son.left
        # make y a child of x, increase the degree of x
        if self.child:
            son.right = self.child
            son.left = self.child.left
            self.child.left.right = son
            self.child.left = son
        else:
            son.right = son
            son.left = son

        self.child = son
        son.parent = self
        self.degree += 1
        son.mark = False

        return self

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
                    #icol = icol - child.ncol()
                    icol = icol - node.ncol()/2
                q.put((level+1, icol, child))
                ochild = child
                while child.right and child.right is not ochild:
                    icol += child.right.ncol()
                    q.put((level+1, icol, child.right))
                    child = child.right

    def pprint(self, colwidth = 6):
        """
        >>> kvs = [(10,)]
        >>> node = binomial_tree(kvs)
        >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
        -10-
        >>> kvs = [(1,), (25,)]
        >>> node = binomial_tree(kvs)
        >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
        -1-
        -25-
        >>> kvs = [(1,), (25,), (12,), (18,)]
        >>> node = binomial_tree(kvs)
        >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
               -1-
        |<12>  <25>|
         -18-
        >>> kvs = [(6,), (29,), (14,), (38,), (8,), (17,), (11,), (27,)]
        >>> node = binomial_tree(kvs)
        >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
                           -6-
              |<8>   <14>  <29>|
        |<11>  <17>| -38-
         -27-
        >>> kvs = [
        ...     (6,), (44,), (10,), (17,), (29,), (31,), (48,), (50,),
        ...     (8,), (22,), (23,), (24,), (30,), (32,), (45,), (55,)
        ... ]
        >>> node = binomial_tree(kvs)
        >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
                                                   -6-
                          |<8>         <29>  <10>  <44>|
              |<30>  <23>  <22>||<48>  <31>| -17-
        |<45>  <32>| -24-        -50-
         -55-
        """
        r = []
        d = {}
        ncol = self.ncol()
        nrow = self.nrow()
        width = ncol * colwidth

        for irow, icol, node in self.bft():
            d.setdefault(irow, {}).update({icol : node})

        for i in range(nrow):
            if i not in d:  # tree of FIB-HEAP won't be a complete binomial tree
                continue    # after decrease_key and delete operation
            tmp = [str(d[i].get(j, '')).ljust(colwidth) for j in range(ncol)]
            r.append(''.join(tmp).rjust(width))

        return '\n'.join(r)

    def __str__(self):
        if self.right is self:
            return ' -%s- ' % self.key
        else:
            if self.parent and self.parent.child is self:
                return '|<%s> ' % self.key
            elif self.parent and self.right is self.parent.child:
                return ' <%s>|' % self.key
            else:
                return ' <%s> ' % self.key

    __repr__ = __str__


def binomial_tree(kvs = []):
    """
    Construct a Binomial tree from a list of k,v pairs, the sequence of the list
    is from right column to left column, each of which from top to bottom.

    >>> kvs = [(10,)]
    >>> node = binomial_tree(kvs)
    >>> list(node.bft())
    [(0, 0,  -10- )]
    >>> kvs = [(6,), (29,), (14,), (38,), (8,), (17,), (11,), (27,)]
    >>> node = binomial_tree(kvs)
    >>> print node.pprint() # doctest: +NORMALIZE_WHITESPACE
                       -6-
          |<8>   <14>  <29>|
    |<11>  <17>| -38-
     -27-
    """
    #heapq.heapify(kvs)
    n = len(kvs)
    if n == 0:
        return None
    elif n == 1:
        return FibonacciNode(*kvs[0])
    elif n == 2:
        return FibonacciNode(*kvs[0]).link_son(FibonacciNode(*kvs[1]))
    elif n%2 == 0:
        m = n/2
        n1 = binomial_tree(kvs[:m])
        n2 = binomial_tree(kvs[m:])
        return n1.link_son(n2)
    else:
        pass


class FibonacciHeap(object):

    def __init__(self, min = None, n = 0):
        self.min = min
        self.n = n

    def build(self, treelist = []):
        """
        Build a Fibonacci heap from a list of binomial tree,
        each of which contains a list of kv pairs.

        >>> H = FibonacciHeap()
        >>> H.build([
        ...     [(10,)],
        ...     [(1,), (25,), (12,), (18,)],
        ...     [(6,), (29,), (14,), (38,), (8,), (17,), (11,), (27,)]
        ... ])
        >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
               <1>                     <6>   <10>
        |<12>  <25>|      |<8>   <14>  <29>|
         -18-       |<11>  <17>| -38-
                     -27-
        """
        if len(treelist) == 0:
            return self
        else:
            self.n += sum([len(e) for e in treelist])
            treelist = [binomial_tree(e) for e in treelist]
            n = len(treelist) - 1
            for i in range(n):
                treelist[i].right = treelist[i+1]
                treelist[i+1].left = treelist[i]
            treelist[0].left = treelist[-1]
            treelist[-1].right = treelist[0]

            m, index = min([(e.key, i) for i,e in enumerate(treelist)])
            self.min = treelist[index]

    def max_degree(self):
        """
        >>> H = FibonacciHeap()
        >>> H.D
        0
        >>> H.insert(FibonacciNode(12))
        >>> H.D
        0
        >>> H.insert(FibonacciNode(8))
        >>> H.D
        1
        """
        return int(math.log(self.n, 2)) if self.n > 0 else 0

    D = property(max_degree)

    def root_list(self):
        """
        >>> H = FibonacciHeap()
        >>> H.build([
        ...     [(10,)],
        ...     [(1,), (25,), (12,), (18,)],
        ...     [(6,), (29,), (14,), (38,), (8,), (17,), (11,), (27,)]
        ... ])
        >>> H.root_list()
        [ <1> ,  <6> ,  <10> ]
        """
        result = []

        min = self.min
        if min:
            result.append(min)

        root = min.right
        while root and root is not min:
            result.append(root)
            root = root.right

        return result

    def insert(self, x):
        """
        Insert node x into the heap after min.

        >>> H = FibonacciHeap()
        >>> H.min
        """
        if not x:
            return

        x.degree = 0
        x.parent = None
        x.child = None
        x.left = x
        x.right = x
        x.mark = False

        if self.min:
            x.left = self.min
            x.right = self.min.right
            self.min.right.left = x
            self.min.right = x
            if x.key < self.min.key:
                self.min = x
        else:
            self.min = x

        self.n += 1

    def minimum(self):
        return self.min

    def union(self, H):
        """
        Union two heaps.

        >>> H1 = FibonacciHeap()
        >>> H1.build([
        ...     [(10,)],
        ...     [(6,), (29,), (14,), (38,), (8,), (17,), (11,), (27,)]
        ... ])
        >>> H2 = FibonacciHeap()
        >>> H2.build([
        ...     [(8,), (15,)],
        ...     [(1,), (25,), (12,), (18,)],
        ... ])
        >>> H1.union(H2)
        >>> print H1.pprint() # doctest: +NORMALIZE_WHITESPACE
               <1>   <8>   <10>                    <6>
        |<12>  <25>| -15-             |<8>   <14>  <29>|
         -18-                   |<11>  <17>| -38-
                                 -27-
        >>> H1.min  # doctest: +NORMALIZE_WHITESPACE
        <1>
        """
        if self.min:
            if H.min:
                H.min.left = self.min
                H.min.right.right = self.min.right
                self.min.right.left = H.min.right
                self.min.right = H.min
                if self.min.key > H.min.key:
                    self.min = H.min
        else:
            self.min = H.min

        self.n += H.n

    def pop(self):
        """
        Extract min.

        >>> H1 = FibonacciHeap()
        >>> H1.build([
        ...     [(10,)],
        ...     [(6,), (29,), (14,), (38,), (8,), (17,), (11,), (27,)]
        ... ])
        >>> H2 = FibonacciHeap()
        >>> H2.build([
        ...     [(8,), (15,)],
        ...     [(1,), (25,), (12,), (18,)],
        ... ])
        >>> H1.union(H2)
        >>> print H1.pprint()  # doctest: +NORMALIZE_WHITESPACE
               <1>   <8>   <10>                    <6>
        |<12>  <25>| -15-             |<8>   <14>  <29>|
         -18-                   |<11>  <17>| -38-
                                 -27-
        >>> H1.pop()  # doctest: +NORMALIZE_WHITESPACE
        <1>
        >>> print H1.pprint()  # doctest: +NORMALIZE_WHITESPACE
                           <6>         <8>   <10>
              |<8>   <14>  <29>||<12>  <15>| -25-
        |<11>  <17>| -38-        -18-
         -27-
        >>> H1.min  # doctest: +NORMALIZE_WHITESPACE
        <6>
        """
        z = self.min
        if z:
            # add children of z into root list
            son = z.child
            if son:
                son.parent = None
                child = son.right
                while child and child is not son:
                    child.parent = None
                    child = child.right
                son.left.right = self.min.right
                self.min.right.left = son.left
                son.left = self.min
                self.min.right = son
                self.min.child = None

            # remove z
            if self.min.left is not self.min:
                self.min.left.right = self.min.right
                self.min.right.left = self.min.left

            if z.right is z:
                self.min = None
            else:
                self.min = z.right
                self.consolidate()

            self.n -= 1

        return z

    def consolidate(self):
        D = self.max_degree()
        A = [None for i in range(D+1)]
        R = self.root_list()
        for w in R:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    tmp = x
                    x = y
                    y = tmp
                self.link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        m, index = min([(e.key, i) for i,e in enumerate(A) if e])
        self.min = A[index]

        #self.min = None
        #for i in range(D+1):
        #    if A[i] is not None:
        #        if self.min:
        #            # remove A[i]
        #            A[i].left.right = A[i].right
        #            A[i].right.left = A[i].left
        #            # add A[i] to root list
        #            A[i].right = self.min.right
        #            A[i].left = self.min
        #            self.min.right.left = A[i]
        #            self.min.right = A[i]
        #        if self.min is None or A[i].key < self.min.key:
        #            self.min = A[i]

    def link(self, y, x):
        """
        Make y a child of x, x.key <= y.key.
        """
        # remove y from root list of self
        y.left.right = y.right
        y.right.left = y.left

        # make y a child of x, increase the degree of x
        if x.child:
            y.right = x.child
            y.left = x.child.left
            x.child.left.right = y
            x.child.left = y
        else:
            y.right = y
            y.left = y

        x.child = y
        y.parent = x
        x.degree += 1
        y.mark = False

    def decrease_key(self, x, k):
        """
        >>> H = FibonacciHeap()
        >>> H.build([
        ...     [(7,), (23,), (17,), (30,), (24,), (46,), (26,), (35,)],
        ...     [(18,), (39,), (21,), (52,)],
        ...     [(38,), (41,)]
        ... ])
        >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
                           <7>         <18>  <38>
              |<24>  <17>  <23>||<21>  <39>| -41-
        |<26>  <46>| -30-        -52-
         -35-
        >>> n46 = H.min.child.child.right
        >>> print n46.pprint() # doctest: +NORMALIZE_WHITESPACE
         <46>|
        >>> H.decrease_key(n46, 15)
        >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
                     <7>   <15>        <18>  <38>
        |<24>  <17>  <23>|      |<21>  <39>| -41-
         -26-  -30-              -52-
         -35-
        >>> n35 = H.min.child.child.child
        >>> n26 = n35.parent
        >>> print n35.pprint() # doctest: +NORMALIZE_WHITESPACE
         -35-
        >>> H.decrease_key(n35, 5)
        >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
         <5>   <15>        <18>  <38>                    <7>
                    |<21>  <39>| -41-       |<24>  <17>  <23>|
                     -52-                    -26-  -30-
        >>> H.decrease_key(n26, 6)
        >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
         <5>   <24>  <6>   <15>        <18>  <38>        <7>
                                |<21>  <39>| -41- |<17>  <23>|
                                 -52-              -30-
        >>> H.min  # doctest: +NORMALIZE_WHITESPACE
        <5>
        >>> n17 = H.min.left.child
        >>> H.decrease_key(n17, 3)
        >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
         <3>   <24>  <6>   <15>        <18>  <38>  <7>   <5>
         -30-                   |<21>  <39>| -41-  -23-
                                 -52-
        """
        if k > x.key:
            print 'new key is greater than current'
            return
        x.key = k
        y = x.parent
        if y and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min.key:
            self.min = x

    def cut(self, x, y):
        x.right.left = x.left
        x.left.right = x.right
        y.degree -= 1
        #y.degree -= x.degree
        #parent = y.parent
        #while parent and parent is not None:
        #    parent.degree -= x.degree
        #    parent = parent.parent

        # remove x from child list of y
        if x.right is not x:
            y.child = x.right
        else:
            y.child = None

        # add x into root list
        self.min.right.left = x
        x.right = self.min.right
        self.min.right = x
        x.left = self.min

        x.parent = None
        x.mark = False

    def cascading_cut(self, y):
        z = y.parent
        if z:
            if y.mark == False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    def delete(self, x):
        """
        >>> H = FibonacciHeap()
        >>> H.build([
        ...     [(7,), (23,), (17,), (30,), (24,), (46,), (26,), (35,)],
        ...     [(18,), (39,), (21,), (52,)],
        ...     [(38,), (41,)]
        ... ])
        >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
                           <7>         <18>  <38>
              |<24>  <17>  <23>||<21>  <39>| -41-
        |<26>  <46>| -30-        -52-
         -35-
        >>> n46 = H.min.child.child.right
        >>> H.delete(n46)
        >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
                     <7>         <18>  <38>
        |<24>  <17>  <23>||<21>  <39>| -41-
         -26-  -30-        -52-
         -35-
        >>> n24 = H.min.child
        >>> H.delete(n24)
        >>> print H.pprint() # doctest: +NORMALIZE_WHITESPACE
               <7>                     <18>
        |<17>  <23>|      |<26>  <21>  <39>|
         -30-       |<38>  <35>| -52-
                     -41-
        """
        self.decrease_key(x, -INF)
        self.pop()

    def nrow(self):
        if not self.min:
            return 0
        min = self.min
        nrow = min.nrow()
        p = min.right

        while p and p is not min:
            prow = p.nrow()
            if prow > nrow:
                nrow = prow
            p = p.right

        return nrow

    def ncol(self):
        if not self.min:
            return 0
        min = self.min
        ncol = min.ncol()
        p = min.right

        while p and p is not min:
            ncol += p.ncol()
            p = p.right

        return ncol

    def bft(self, level = 0):
        """Breadth first traversal."""
        q = Queue.Queue()

        if not self.min:
            yield self.min

        min = self.min
        icol = min.ncol() - 1
        q.put((level, icol, min))
        p = min.right

        while p and p is not min:
            if p:
                icol += p.ncol()
            q.put((level, icol, p))
            p = p.right

        while not q.empty():
            level, icol, node = q.get()
            yield (level, icol, node)
            child = node.child
            if child:
                if node.degree > 1:
                    #icol = icol - child.ncol()
                    icol = icol - node.ncol()/2
                q.put((level+1, icol, child))
                ochild = child
                while child.right and child.right is not ochild:
                    icol += child.right.ncol()
                    q.put((level+1, icol, child.right))
                    child = child.right

    def pprint(self, colwidth = 6):
        """
        Pretty print.
        """
        if not self.min:
            return
        r = []
        d = {}
        ncol = self.ncol()
        nrow = self.nrow()
        width = ncol * colwidth

        for irow, icol, node in self.bft():
            d.setdefault(irow, {}).update({icol : node})

        for i in range(nrow):
            if i not in d:
                continue
            tmp = [str(d[i].get(j, '')).ljust(colwidth) for j in range(ncol)]
            r.append(''.join(tmp).rjust(width))

        return '\n'.join(r)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
