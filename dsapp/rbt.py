#! /usr/bin/env python
# coding: utf-8

from rbtree import rbtree

def keys_range(self, kmin, kmax):
    result = []
    
    ck = self.ceiling_key(kmin)
    while ck < kmax:
        result.append(ck)
        ck = self.succ_key(ck)
    
    return result

rbtree.keys_range = keys_range

def values_range(self, kmin, kmax):
    result = []
    
    ck = self.ceiling_key(kmin)
    while ck < kmax:
        result.append(self[ck])
        ck = self.succ_key(ck)
    
    return result

rbtree.values_range = values_range

def items_range(self, kmin, kmax):
    result = []
    
    ck = self.ceiling_key(kmin)
    while ck < kmax:
        result.append((ck, self[ck]))
        ck = self.succ_key(ck)
    
    return result

rbtree.items_range = items_range

if __name__ == '__main__':
    pass

