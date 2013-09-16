#! /usr/bin/env python
# coding: utf-8

"""
Graph.

Reference:

- Introduction to Algorithms.
- http://interactivepython.org/runestone/static/pythonds/Graphs/graphintro.html

"""

import Queue
from pprint import pprint

INF = float('inf')
WHITE = 'WHITE'
GREY = 'GREY'
BLACK = 'BLACK'


class Vertex:
    
    def __init__(self,key):
        self.id = key
        self.neighbors = {}
        #self.color = WHITE
        #self.distant = INF
        #self.parent = None
        #self.dtime = 0
        #self.ftime = 0

    def add_neighbor(self, vertex, weight=0):
        self.neighbors[vertex] = weight

    def __str__(self):
        return str(self.id) + ' neighbors: ' + str([x.id for x in self.neighbors])

    __repr__ = __str__
    
    def get_neighbors(self):
        return self.neighbors.keys()

    def get_id(self):
        return self.id

    def get_weight(self, vertex):
        return self.neighbors[vertex]


class Graph:
    
    def __init__(self):
        """
        >>> g = Graph()
        >>> tmp = [g.add_vertex(i) for i in range(6)]
        >>> g.vertices           # doctest: +SKIP
        >>> edges = [
        ...     (0,1,5),(0,5,2),(1,2,4),
        ...     (2,3,9),(3,4,7),(3,5,3),
        ...     (4,0,1),(5,4,8),(5,2,1)
        ... ]
        >>> for e in edges:
        ...     g.add_edge(*e)
        """
        self.vertices = {}
        self.nv = 0
        self.time = 0

    def add_vertex(self, key):
        self.nv = self.nv + 1
        v = Vertex(key)
        self.vertices[key] = v
        return v

    def get_vertex(self, key):
        if key in self.vertices:
            return self.vertices[key]
        else:
            #raise Exception('vertex not in graph')
            return None
    __getitem__ = get_vertex

    def __contains__(self,n):
        return n in self.vertices

    def add_edge(self, f, t, cost=0):
        """Digraph."""
        if f not in self.vertices:
            nv = self.add_vertex(f)
        if t not in self.vertices:
            nv = self.add_vertex(t)
        self.vertices[f].add_neighbor(self.vertices[t], cost)

    def __iter__(self):
        return iter(self.vertices.values())

    def bfs(self, s):
        """
        >>> g = Graph()
        >>> tmp = [g.add_vertex(i) for i in range(6)]
        >>> g.vertices           # doctest: +SKIP
        >>> edges = [
        ...     (0,1,5),(0,5,2),(1,2,4),
        ...     (2,3,9),(3,4,7),(3,5,3),
        ...     (4,0,1),(5,4,8),(5,2,1)
        ... ]
        >>> for e in edges:
        ...     g.add_edge(*e)
        >>> g.bfs(g[0])
        >>> pprint([(v.id,v.color,v.distant) for v in g.vertices.itervalues()])
        [(0, 'BLACK', 0),
         (1, 'BLACK', 1),
         (2, 'BLACK', 2),
         (3, 'BLACK', 3),
         (4, 'BLACK', 2),
         (5, 'BLACK', 1)]
        """
        if not s:
            return
        for e in self.vertices.itervalues():
            e.color = WHITE
            e.distant = INF
            e.parent = None
            
        s.color = GREY
        s.distant = 0
        s.parent = None
        
        q = Queue.Queue()
        q.put(s)
        while not q.empty():
            v = q.get()
            for e in v.neighbors:
                if e.color == WHITE:
                    e.color = GREY
                    e.distant = v.distant + 1
                    e.parent = v
                    q.put(e)
            v.color = BLACK

    def dfs(self, keys = None):
        """
        >>> g = Graph()
        >>> tmp = [g.add_vertex(i) for i in range(6)]
        >>> g.vertices           # doctest: +SKIP
        >>> edges = [
        ...     (0,1,5),(0,5,2),(1,2,4),
        ...     (2,3,9),(3,4,7),(3,5,3),
        ...     (4,0,1),(5,4,8),(5,2,1)
        ... ]
        >>> for e in edges:
        ...     g.add_edge(*e)
        >>> [v.id for v in g.dfs()]
        [0]
        >>> pprint([(v.id,v.color,v.dtime,v.ftime) for v in g.vertices.itervalues()])    #doctest: +SKIP
        [(0, 'BLACK', 1, 12),
         (1, 'BLACK', 10, 11),
         (2, 'BLACK', 5, 8),
         (3, 'BLACK', 6, 7),
         (4, 'BLACK', 3, 4),
         (5, 'BLACK', 2, 9)]
        >>> g = Graph()
        >>> tmp = [g.add_vertex(i) for i in list('ABCDEFGHI')]
        >>> g.vertices           # doctest: +SKIP
        >>> edges = [
        ...     ('A','B',5),('B','C',2),('C','F',4),
        ...     ('F','H',5),('H','I',2),('I','F',4),
        ...     ('B','E',5),('E','D',2),('D','B',4),
        ...     ('E','A',5),('D','G',2),('G','E',4),
        ... ]
        >>> for e in edges:
        ...     g.add_edge(*e)
        >>> [v.id for v in g.dfs()]
        ['A']
        """
        roots = []
        
        for e in self.vertices.itervalues():
            e.color = WHITE
            e.parent = None
        self.time = 0
        if not keys:
            keys = self.vertices.keys()
        for k in keys:
            v = self[k]
            if v.color == WHITE:
                self.dfs_visit(v)
                roots.append(v)
        
        return roots
    
    def dfs_visit(self, s):
        s.color = GREY
        self.time += 1
        s.dtime = self.time
        for v in s.neighbors:
            if v.color == WHITE:
                v.parent = s
                self.dfs_visit(v)
        s.color = BLACK
        self.time += 1
        s.ftime = self.time

    def topological_sort(self):
        """
        >>> g = Graph()
        >>> vertices = [
        ...     'shirt', 'tie', 'jacket', 'belt', 'pants',
        ...     'undershorts','shoes', 'socks', 'watch',
        ... ]
        >>> tmp = [g.add_vertex(i) for i in vertices]
        >>> g.vertices           # doctest: +SKIP
        >>> edges = [
        ...     ('undershorts','pants',5),('undershorts','shoes',2),
        ...     ('socks','shoes',4),('pants','shoes',4),('pants','belt',4),
        ...     ('shirt','belt',4),('belt','jacket',4),('shirt','tie',4),
        ...     ('tie','jacket',4),
        ... ]
        >>> for e in edges:
        ...     g.add_edge(*e)
        >>> pprint(g.topological_sort())   #doctest: +SKIP
        [('undershorts', 15, 18),
         ('pants', 16, 17),
         ('socks', 13, 14),
         ('shoes', 11, 12),
         ('watch', 9, 10),
         ('shirt', 1, 8),
         ('belt', 6, 7),
         ('tie', 2, 5),
         ('jacket', 3, 4)]
        """
        self.dfs()
        
        result = sorted(
            [(v.id, v.dtime, v.ftime) for v in self.vertices.itervalues()], 
            key = lambda e:e[2], 
            reverse = True
        )
        
        return result

    def transpose(self):
        """
        >>> g = Graph()
        >>> vertices = [
        ...     'shirt', 'tie', 'jacket', 'belt', 'pants',
        ...     'undershorts','shoes', 'socks', 'watch',
        ... ]
        >>> tmp = [g.add_vertex(i) for i in vertices]
        >>> g.vertices           # doctest: +SKIP
        >>> edges = [
        ...     ('undershorts','pants',5),('undershorts','shoes',2),
        ...     ('socks','shoes',4),('pants','shoes',4),('pants','belt',4),
        ...     ('shirt','belt',4),('belt','jacket',4),('shirt','tie',4),
        ...     ('tie','jacket',4),
        ... ]
        >>> for e in edges:
        ...     g.add_edge(*e)
        >>> gt = g.transpose()
        >>> pprint(gt.topological_sort())    #doctest: +SKIP
        [('shoes', 17, 18),
         ('jacket', 11, 16),
         ('tie', 14, 15),
         ('belt', 12, 13),
         ('socks', 9, 10),
         ('pants', 5, 8),
         ('undershorts', 6, 7),
         ('watch', 3, 4),
         ('shirt', 1, 2)]
        """
        gt = Graph()
        
        for k in self.vertices:
            gt.add_vertex(k)
        for k in self.vertices:
            for v,w in self[k].neighbors.iteritems():
                gt.add_edge(v.id, k, w)
        
        return gt

    def scc(self):
        """
        Strongly connected components.
        
        >>> g = Graph()
        >>> tmp = [g.add_vertex(i) for i in list('ABCDEFGHI')]
        >>> g.vertices           # doctest: +SKIP
        >>> edges = [
        ...     ('A','B',5),('B','C',2),('C','F',4),
        ...     ('F','H',5),('H','I',2),('I','F',4),
        ...     ('B','E',5),('E','D',2),('D','B',4),
        ...     ('E','A',5),('D','G',2),('G','E',4),
        ... ]
        >>> for e in edges:
        ...     g.add_edge(*e)
        >>> pprint(g.scc())
        {'A': ['A', 'B', 'E', 'D', 'G'], 'C': ['C'], 'F': ['F', 'I', 'H']}
        """
        trees = {}
        
        self.dfs()
        keys = [e[0] for e in self.topological_sort()]
        gt = self.transpose()
        roots = gt.dfs(keys)
        for v in gt.vertices.itervalues():
            for root in roots:
                if root.dtime <= v.dtime and root.ftime >= v.ftime:
                    trees.setdefault(root.id, []).append(v.id)
                    break
        
        return trees

if __name__ == '__main__':
    import doctest
    doctest.testmod()
