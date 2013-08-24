#! /usr/bin/env python
# coding: utf-8

# based on chapter 18 of Introduction to Algorithms(Second Edition)

import bisect
import Queue

try:
    from blist import blist
except:
    pass


class BNode(object):

    def __init__(self):
        # Will be better with deque or blist?
        self.keys = list()
        self.children = list()
        self.data = {}

    def is_leaf(self):
        return not bool(self.children)

    def __str__(self):
        return '(%s)' % ','.join([str(e) for e in self.keys])

    def __repr__(self):
        return '(%s)' % ','.join([str(e) for e in self.keys])


class BTree(object):

    def __init__(self, degree = 3):
        self.degree = degree
        self.root = BNode()

        self._minkeys = self.degree - 1
        self._minchildren = self.degree
        self._maxkeys = 2 * self.degree - 1
        self._maxchildren = 2 * self.degree
        #self.disk_write(self.root)

    def search(self, node, key):
        i = bisect.bisect_left(node.keys, key)
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)
        if node.is_leaf():
            return (None, None)
        else:
            # self.disk_read(node.children[i])
            return self.search(node.children[i], key)

    def ceiling(self, node, key):
        i = bisect.bisect_left(node.keys, key)
        if i < len(node.keys) and key == node.keys[i]:
            return key
        if node.is_leaf():
            if i == len(node.keys):
                return node.keys[-1]
            return node.keys[i]
        else:
            return self.ceiling(node.children[i], key)

    def split_child(self, x, i, y):
        z = BNode()
        z.keys = y.keys[self.degree:]
        z.data = dict([(k, y.data[k]) for k in z.keys])
        if not y.is_leaf():
            z.children = y.children[self.degree:]
        x.children.insert(i+1, z)
        mk = y.keys[self.degree-1]
        x.keys.insert(i, mk)
        mv = y.data.get(mk)
        if mv:
            x.data[mk] = mv
        y.keys = y.keys[:self.degree-1]
        y.data = dict([(k, y.data[k]) for k in y.keys])
        y.children = y.children[:self.degree]
        #self.disk_write(y)
        #self.disk_write(z)
        #self.disk_write(x)

    def insert(self, key, value = None):
        if len(self.root.keys) == self._maxkeys:
            oldroot = self.root
            self.root = BNode()
            self.root.children.append(oldroot)
            self.split_child(self.root, 0, oldroot)
            self.insert_nonfull(self.root, key, value)
        else:
            self.insert_nonfull(self.root, key, value)

    def insert_nonfull(self, x, key, value = None):
        i = len(x.keys)
        # performance bottleneck
        #while i > 0 and key < x.keys[i-1]:
        #    i -= 1
        i = bisect.bisect_left(x.keys, key)
        if x.is_leaf():
            x.keys.insert(i, key)
            if value:
                x.data.setdefault(key, value)
            #self.disk_write(x)
        else:
            #self.disk_read(x.children[i])
            if len(x.children[i].keys) == self._maxkeys:
                self.split_child(x, i, x.children[i])
                if key > x.keys[i]:
                    i += 1
            self.insert_nonfull(x.children[i], key, value)

    def delete(self, node, key):
        if key in node.keys:
            if node.is_leaf():
                node.keys.remove(key)
                node.data.pop(key, None)
            else:
                ki = node.keys.index(key)
                if len(node.children[ki].keys) >= self.degree:
                    kp = node.children[ki].keys[-1]
                    vp = node.children[ki].data.pop(kp, None)
                    self.delete(node, kp)
                    node.keys[ki] = kp
                    if vp:
                        node.data[kp] = vp
                elif len(node.children[ki+1].keys) >= self.degree:
                    kp = node.children[ki+1].keys[0]
                    vp = node.children[ki+1].data.pop(kp, None)
                    self.delete(node, kp)
                    node.keys[ki] = kp
                    if vp:
                        node.data[kp] = vp
                else:
                    node.children[ki].keys.append(node.keys.pop(ki))
                    v = node.data.pop(key, None)
                    if v:
                        node.children[ki].data[key] = v
                    rnode = node.children.pop(ki+1)
                    node.children[ki].keys.extend(rnode.keys)
                    node.children[ki].data.update(rnode.data)
                    node.children[ki].children.extend(rnode.children)
                    if node == self.root and not node.keys:
                        self.root = node.children[ki]
                    self.delete(node.children[ki], key)
        else:
            ci = bisect.bisect_left(node.keys, key)
            if len(node.children[ci].keys) == self._minkeys:
                if ci > 1 and len(node.children[ci-1].keys) > self._minkeys:
                    kp = node.children[ci-1].keys.pop(-1)
                    vp = node.children[ci-1].data.pop(kp, None)
                    node.keys.insert(0, kp)
                    if vp:
                        node.data[kp] = vp
                    node.children[ci].keys.insert(0, node.keys.pop(-1))
                    self.delete(node.children[ci], key)
                elif ci < len(node.keys) and len(node.children[ci+1].keys) > self._minkeys:
                    kp = node.children[ci+1].keys.pop(0)
                    vp = node.children[ci+1].data.pop(kp, None)
                    node.keys.append(kp)
                    if vp:
                        node.data[kp] = vp
                    node.children[ci].keys.append(node.keys.pop(0))
                    self.delete(node.children[ci], key)
                else:
                    if ci >= 1:
                        kp = node.keys.pop(ci-1)
                        vp = node.data.pop(kp, None)
                        node.children[ci-1].keys.append(kp)
                        if vp:
                            node.children[ci-1].data[kp] = vp
                        rnode = node.children.pop(ci)
                        node.children[ci-1].keys.extend(rnode.keys)
                        node.children[ci-1].data.extend(rnode.data)
                        node.children[ci-1].children.extend(rnode.children)
                        if node == self.root and not node.keys:
                            self.root = node.children[ci-1]
                        self.delete(node.children[ci-1], key)
                    else:
                        kp = node.keys.pop(ci)
                        vp = node.data.pop(kp, None)
                        node.children[ci].keys.append(kp)
                        if vp:
                            node.children[ci].data[kp] = vp
                        rnode = node.children.pop(ci+1)
                        node.children[ci].keys.extend(rnode.keys)
                        node.children[ci].data.extend(rnode.data)
                        node.children[ci].children.extend(rnode.children)
                        if node == self.root and not node.keys:
                            self.root = node.children[ci]
                        self.delete(node.children[ci], key)
            else:
                self.delete(node.children[ci], key)

    def keys(self, kmin = None, kmax = None):
        keys = []
        
        if kmin is None:
            kmin = self.min()
        if kmax is None:
            kmax = self.max()
        
        return self._keys(self.root, keys, kmin, kmax)

    def _keys(self, node, keys, kmin, kmax):
        """return [key for key in allkeys if kmin <= keys <= kmax]"""
        imin = bisect.bisect_left(node.keys, kmin)
        imax = bisect.bisect_left(node.keys, kmax)

        if node.children:
            for e in node.children[imin:imax+1]:
                self._keys(e, keys, kmin, kmax)
        keys.extend(node.keys[imin:imax])
        if node.keys[imax-1] == kmax:
            keys.append(kmax)

        return keys

    def min(self):
        node = self.root
        while node.children:
            node = node.children[0]
        return node.keys[0]

    def max(self):
        node = self.root
        while node.children:
            node = node.children[-1]
        return node.keys[-1]

    def bft(self, node, level = 1):
        """Breadth first traversal."""
        q = Queue.Queue()
        level = level
        q.put((level, node))

        while not q.empty():
            level, node = q.get()
            yield (level, node)
            for e in node.children:
                q.put((level+1, e))

    def levels(self):
        leveldict = {}

        for level, node in self.bft(self.root):
            leveldict.setdefault(level, []).append(node)

        return leveldict

    def pprint(self, data = False, width = 80):
        leveldict = self.levels()
        keys = leveldict.keys()
        for k in keys:
            if data:
                print ' '.join(str(e.data) for e in leveldict[k]).center(width)
            else:
                print ' '.join(str(e) for e in leveldict[k]).center(width)

    def __setitem__(self, k, v):
        self.insert(k, v)

    def __getitem__(self, k):
        node, i = self.search(self.root, k)
        if node:
            return node.data.get(node.keys[i], None)
        else:
            return None

    def __delitem__(self, k):
        self.delete(self.root, k)


if __name__ == '__main__':
    from pprint import pprint
    b = BTree(2)
    kv = [
        (0, 'zero'),
        (8, 'eight'),
        (9, 'nine'),
        (1, 'one'),
        (7, 'seven'),
        (2, 'two'),
        (6, 'six'),
        (3, 'three'),
        (5, 'five'),
        (4, 'four'),
    ]
    for k, v in kv:
        b[k] = v
    b.pprint(True)
    del b[1]
    b.pprint(True)
    print b[5.5]
    print 'min key: ', b.min()
    print 'max key: ', b.max()
    print 'ceiling: ', b.ceiling(b.root, 9.4)
    #print b.keys()
    #print b.keys(2.2, 7.8)
    print b.keys()
    print b.keys(3, 6)