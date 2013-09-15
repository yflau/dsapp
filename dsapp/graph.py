#! /usr/bin/env python
# coding: utf-8

"""
Disjoint set.

Reference:

- Introduction to Algorithms.
- http://interactivepython.org/runestone/static/pythonds/Graphs/graphintro.html

"""

class Vertex:
    
    def __init__(self,key):
        self.id = key
        self.neighbors = {}

    def add_neighbor(self, vertex, weight=0):
        self.neighbors[vertex] = weight

    def __str__(self):
        return str(self.id) + ' neighbors: ' + str([x.id for x in self.neighbors])

    def get_neighbors(self):
        return self.neighbors.keys()

    def get_id(self):
        return self.id

    def get_weight(self,nbr):
        return self.neighbors[nbr]


class Graph:
    
    def __init__(self):
        """
        >>> g = Graph()
        >>> tmp = [g.add_vertex(i) for i in range(6)]
        >>> g.vertices           # doctest: +SKIP
        >>> g.add_edge(0,1,5)
        >>> g.add_edge(0,5,2)
        >>> g.add_edge(1,2,4)
        >>> g.add_edge(2,3,9)
        >>> g.add_edge(3,4,7)
        >>> g.add_edge(3,5,3)
        >>> g.add_edge(4,0,1)
        >>> g.add_edge(5,4,8)
        >>> g.add_edge(5,2,1)
        >>> for v in g:
        ...    for w in v.get_neighbors():
        ...        print("( %s , %s )" % (v.id, w.id))
        ...
        ( 0 , 1 )
        ( 0 , 5 )
        ( 1 , 2 )
        ( 2 , 3 )
        ( 3 , 4 )
        ( 3 , 5 )
        ( 4 , 0 )
        ( 5 , 4 )
        ( 5 , 2 )
        """
        self.vertices = {}
        self.nv = 0

    def add_vertex(self, key):
        self.nv = self.nv + 1
        v = Vertex(key)
        self.vertices[key] = v
        return v

    def get_vertex(self,n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertices

    def add_edge(self,f,t,cost=0):
        if f not in self.vertices:
            nv = self.add_vertex(f)
        if t not in self.vertices:
            nv = self.add_vertex(t)
        self.vertices[f].add_neighbor(self.vertices[t], cost)

    def get_vertices(self):
        return self.vertices.keys()

    def __iter__(self):
        return iter(self.vertices.values())



if __name__ == '__main__':
    import doctest
    doctest.testmod()

