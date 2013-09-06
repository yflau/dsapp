#
# Copyright 2000 Mats Kindahl. All rights reserved.
#
# This code is in the public domain. Use this code at your own risk,
# there is NO WARRANTY for correctness or for being suitable for any
# particular purpose. 
#
# Class implementing the Disjoint Set forests for implementation of
# UNION/FIND algorithms with path compression and union by rank
# optimizations.

class Node:
    def __init__(self):
        "Constructor. Inherit from this class to add data."
        self.__parent = self
        self.__rank = 0

    def find(self):
        """Find the representative for the set self is in.
        if x.find() == y.find(), then x and y are in the same set."""
        if self != self.__parent:
            self.__parent = self.__parent.find()
        return self.__parent

    def _linkWith(x,y):
        """Private method to link two nodes into the same set.
        The nodes have to be root nodes of their respective sets.
        """
        assert x.__parent == x and y.__parent == y
        if x.__rank > y.__rank:
            y.__parent = x
        else:
            x.__parent = y
            if x.__rank == y.__rank:
                y.__rank = y.__rank + 1
                
    def mergeWith(x,y):
        "Public method to merge the sets x and y are in."
        x.find()._linkWith(y.find())

def merge(x,y):
    "Helpful function to merge the sets x and y are in."
    x.mergeWith(y)

if __name__ == '__main__':
    a = []
    for i in xrange(0,10):
        a.append(Node())
    for i in xrange(0,9):
        if a[i].find() == a[i+1].find():
            print "Something's wrong:", i, "and",
            print i+1, "are in the same set."

        merge(a[i],a[i+1])

        if a[i].find() != a[i+1].find():
            print "Something's wrong:", i, "and",
            print i+1, "are *not* in the same set."
        
