#! /usr/bin/env python
# coding: utf-8

from rbtree import rbtree

def search_range(self, kmin, kmax):
    result = []
    
    for k, v in self.iteritems():
        if kmin < k < kmax:
            result.append(k)
    
    return result

rbtree.search_range = search_range
