#! /usr/bin/env python
# coding: utf-8

"""
Disjoint set.

Reference:

- Introduction to Algorithms.

"""

import random

################################################################################


class ufdict(object):
    """
    From: http://code.activestate.com/recipes/215912/, fixed a bug.
    """
    
    def __init__(self, elements = []):
        """
        >>> vertices = range(9)
        >>> edges = [(5,4), (6,3), (6,2), (1,8), (3,4), (1,0)]
        >>> uf = ufdict(vertices)
        >>> sorted(list(uf))
        [[0], [1], [2], [3], [4], [5], [6], [7], [8]]
        >>> tmp = [uf.union(u, v) for u,v in edges]
        >>> sorted(list(uf))
        [[2, 3, 4, 5, 6], [7], [8, 1, 0]]
        >>> uf.count
        3
        """
        self.objects = {e:{e:1} for e in elements}
        self.count = len(self.objects)
            
    def find(self, a):
        if a not in self.objects:
            self.objects[a] = {a:1}
            self.count += 1
        return id(self.objects[a])
        
    def union(self, a, b):
        if self.find(a) != self.find(b):
            la = len(self.objects[a])
            lb = len(self.objects[b])
            if la > lb:
                a, b = b, a
            self.objects[b].update(self.objects[a])
            for e in self.objects[a]:
                self.objects[e] = self.objects[b]
            self.count -= 1

    def __iter__(self):
        outp = {}
        for i in self.objects.itervalues():
            outp[id(i)] = i
        for i in outp.values():
            yield i.keys()

    def __str__(self):
        return ', '.join([str(e) for e in list(self)])

    __repr__ = __str__

################################################################################

class UnionFind:

    def __init__(self):
        '''
        Create an empty union find data structure.

        >>> vertices = range(9)
        >>> edges = [(5,4), (6,3), (6,2), (1,8), (3,4), (1,0)]
        >>> uf = UnionFind()
        >>> [uf.find(v) for v in vertices]
        [0, 1, 2, 3, 4, 5, 6, 7, 8]
        >>> uf
        [0], [1], [2], [3], [4], [5], [6], [7], [8]
        >>> tmp = [uf.union(u, v) for u,v in edges]
        >>> uf
        [0, 1, 8], [2, 3, 4, 5, 6], [7]
        >>> list(uf)
        [[0, 1, 8], [2, 3, 4, 5, 6], [7]]
        '''
        self.num_weights = {}
        self.parent_pointers = {}
        self.num_to_objects = {}
        self.objects_to_num = {}
        self.__repr__ = self.__str__

    def insert_objects(self, objects):
        '''
        Insert a sequence of objects into the structure.  All must be Python hashable.
        '''
        for object in objects:
            self.find(object)

    def find(self, object):
        '''
        Find the root of the set that an object is in.
        If the object was not known, will make it known, and it becomes its own set.
        Object must be Python hashable.
        '''
        if not object in self.objects_to_num:
            obj_num = len(self.objects_to_num)
            self.num_weights[obj_num] = 1
            self.objects_to_num[object] = obj_num
            self.num_to_objects[obj_num] = object
            self.parent_pointers[obj_num] = obj_num
            return object
        stk = [self.objects_to_num[object]]
        par = self.parent_pointers[stk[-1]]
        while par != stk[-1]:
            stk.append(par)
            par = self.parent_pointers[par]
        for i in stk:
            self.parent_pointers[i] = par
        return self.num_to_objects[par]

    def union(self, object1, object2):
        '''
        Combine the sets that contain the two objects given.
        Both objects must be Python hashable.
        If either or both objects are unknown, will make them known, and combine them.
        '''
        o1p = self.find(object1)
        o2p = self.find(object2)
        if o1p != o2p:
            on1 = self.objects_to_num[o1p]
            on2 = self.objects_to_num[o2p]
            w1 = self.num_weights[on1]
            w2 = self.num_weights[on2]
            if w1 < w2:
                o1p, o2p, on1, on2, w1, w2 = o2p, o1p, on2, on1, w2, w1
            self.num_weights[on1] = w1+w2
            del self.num_weights[on2]
            self.parent_pointers[on2] = on1

    def __iter__(self):
        sets = {}
        for i in xrange(len(self.objects_to_num)):
            sets[i] = []
        for i in self.objects_to_num:
            sets[self.objects_to_num[self.find(i)]].append(i)
        for i in sets.itervalues():
            if i:
                yield i

    def __str__(self):
        '''
        Included for testing purposes only.
        All information needed from the union find data structure can be attained
        using find.
        '''
        return ', '.join([repr(i) for i in list(self)])

################################################################################

class ufset(object):
    """
    From: http://pyalda.com/data-types/general/disjoint-sets.html
    """
    
    def __init__(self, elements = []):
        """
        >>> vertices = range(9)
        >>> edges = [(5,4), (6,3), (6,2), (1,8), (3,4), (1,0)]
        >>> uf = ufset(vertices)
        >>> tmp = [uf.union(u, v) for u,v in edges]
        >>> uf.sets
        set([frozenset([2, 3, 4, 5, 6]), frozenset([7]), frozenset([8, 1, 0])])
        """
        self.sets = set([frozenset([e]) for e in elements])
        
    def find(self, x):
        """Bottleneck."""
        for subset in self.sets:
            if x in subset:
                return subset
                
        subset = frozenset([x])
        self.sets.add(subset)
        return subset
    
    def union(self, x, y):
        setx = self.find(x)
        sety = self.find(y)
        if setx is not sety:
            self.sets.add(frozenset.union(setx, sety))
            self.sets.remove(setx)
            self.sets.remove(sety)
    
    def __iter__(self):
        for e in self.sets:
            yield e
    
    def __str__(self):
        return str(self.sets)
    
    __repr__ = __str__

################################################################################

class uflist(object):
    """
    From: http://pyalda.com/data-types/general/disjoint-sets.html
    """

    def __init__(self, elements = []):
        """
        >>> vertices = range(9)
        >>> edges = [(5,4), (6,3), (6,2), (1,8), (3,4), (1,0)]
        >>> uf = uflist(vertices)
        >>> tmp = [uf.union(u, v) for u,v in edges]
        >>> uf
        [[1, 8, 0], [6, 3, 2, 5, 4], [7]]
        """
        self.sets = [[e] for e in elements]
        self.lookup = {e:i for i,e in enumerate(elements)}
    
    def find(self, x):
        if x in self.lookup:
            return self.lookup[x]
        else:
            self.sets.append([x])
            index = len(self.sets) - 1
            self.lookup[x] = index
            return index
    
    def union(self, x, y):
        setx = self.lookup[x]
        sety = self.lookup[y]
        if setx is not sety:
            if self.sets[setx] is not None and self.sets[sety] is not None:
                self.sets[setx].extend(self.sets[sety])
                for k in self.sets[sety]:
                    self.lookup[k] = setx
                self.sets[sety] = None

    def __iter__(self):
        sets = filter(None, self.sets)
        for e in sets:
            yield e
    
    def __str__(self):
        return str(list(self))
    
    __repr__ = __str__

################################################################################

def test_ufdict(edges, vertices):
    uf = ufdict(vertices)

    for (u, v) in edges:
        uf.union(u, v)

    return list(uf)

def test_UnionFind(edges, vertices):
    # main algorithm: find all connected components
    uf = UnionFind()
    for v in vertices:
        uf.find(v)

    for (u, v) in edges:
        uf.union(u, v)

    return list(uf)

def test_ufset(edges, vertices):
    uf = ufset(vertices)
    for (u, v) in edges:
        uf.union(u, v)

    return uf.sets

def test_uflist(edges, vertices):
    uf = uflist(vertices)
    for (u, v) in edges:
        uf.union(u, v)

    return list(uf)

def test():
    """
    20,000 vertices and 4,000 edges
                      test_ufset:        15.44 for result  16001
                     test_ufdict:         0.09 for result  16001
                     test_uflist:         0.03 for result  16001
                  test_UnionFind:         0.09 for result  16001
                    
    1,000,00 vertices and 20,000 edges
                     test_ufdict:         0.59 for result  80001
                     test_uflist:         0.22 for result  80001
                  test_UnionFind:         0.64 for result  80001
    
    1,000,000 vertices and 200,000 edges
                     test_ufdict:        11.30 for result 800000
                     test_uflist:         2.97 for result 800000
                  test_UnionFind:         7.03 for result 800000
    """
    import time

    # see above: test data parameters
    SIZE_OF_DOMAIN = 10000
    SIZE_OF_EDGES = 2000

    edges = [(random.randrange(SIZE_OF_DOMAIN), random.randrange(SIZE_OF_DOMAIN)) for k in range(SIZE_OF_EDGES)]
    vertices = range(SIZE_OF_DOMAIN)

    functions = {
        'test_ufdict' : test_ufdict,
        'test_UnionFind' : test_UnionFind,
        'test_ufset' : test_ufset,
        'test_uflist' : test_uflist,
    }

    expected_result = None
    for function_name in functions:
        function = functions[function_name]
        t0 = time.time()
        result = len(function(edges, vertices))
        t0 = time.time() - t0
        print "%32s: %12.2f for result %6d" % (function_name, t0, result, )

        if expected_result is None:
            expected_result = result
        else:
            assert result == expected_result

################################################################################


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    test()

