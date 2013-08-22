#! /usr/bin/env python
# coding: utf-8

# based on chapter 18 of Introduction to Algorithms(Second Edition)

import bisect

class BNode(object):
    
    def __init__(self):
        self.keys = []
        self.children = []
        self.isLeaf = True
        #self.values = []
        
    def __str__(self):
        return '(%s)' % ','.join([str(e) for e in self.keys])

    def __repr__(self):
        return '(%s)' % ','.join([str(e) for e in self.keys])

class BTree(object):
    
    def __init__(self, order = 3):
        self.order = order
        self.root = BNode()
        self._minkeys = self.order - 1
        self._minchildren = self.order
        self._maxkeys = 2 * self.order - 1
        self._maxchildren = 2 * self.order
        #self.disk_write(self.root)
        
    def search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)
        if node.isLeaf:
            return None
        else:
            # self.disk_read(node.children[i])
            return self.search(node.children[i], key)

    def split_child(self, x, i, y):
        z = BNode()
        z.isLeaf = y.isLeaf
        z.keys = y.keys[self.order:]
        if not y.isLeaf:
            z.children = y.children[self.order:]
        x.children.insert(i+1, z)
        x.keys.insert(i, y.keys[self.order-1])
        y.keys = y.keys[:self.order-1]
        y.children = y.children[:self.order]
        #self.disk_write(y)
        #self.disk_write(z)
        #self.disk_write(x)

    def insert(self, key):
        if len(self.root.keys) == self._maxkeys:
            oldroot = self.root
            self.root = BNode()
            self.root.isLeaf = False
            self.root.children.append(oldroot)
            self.split_child(self.root, 0, oldroot)
            self.insert_nonfull(self.root, key)
        else:
            self.insert_nonfull(self.root, key)
            
    def insert_nonfull(self, x, key):
        i = len(x.keys)
        while i > 0 and key < x.keys[i-1]:
            i -= 1
        if x.isLeaf:
            x.keys.insert(i, key)
            #self.disk_write(x)
        else:
            #self.disk_read(x.children[i])
            if len(x.children[i].keys) == self._maxkeys:
                self.split_child(x, i, x.children[i])
                if key > x.keys[i]:
                    i += 1
            self.insert_nonfull(x.children[i], key)

    def delete(self, node, key):
        if key in node.keys:
            if node.isLeaf:
                node.keys.remove(key)
            else:
                ki = node.keys.index(key)
                if len(node.children[ki].keys) >= self.order:
                    kp = node.children[ki].keys[-1]
                    self.delete(node, kp)
                    node.keys[ki] = kp
                elif len(node.children[ki+1].keys) >= self.order:
                    kp = node.children[ki+1].keys[0]
                    self.delete(node, kp)
                    node.keys[ki] = kp
                else:
                    node.children[ki].keys.append(node.keys.pop(ki))
                    rnode = node.children.pop(ki+1)
                    node.children[ki].keys.extend(rnode.keys)
                    node.children[ki].children.extend(rnode.children)
                    if node == self.root and not node.keys:
                        self.root = node.children[ki]
                    self.delete(node.children[ki], key)
        else:
            ci = bisect.bisect_left(node.keys, key)
            if len(node.children[ci].keys) == self._minkeys:
                if ci > 1 and len(node.children[ci-1].keys) > self._minkeys:
                    node.keys.insert(0, node.children[ci-1].keys.pop(-1))
                    node.children[ci].keys.insert(0, node.keys.pop(-1))
                    self.delete(node.children[ci], key)
                elif ci < len(node.keys) and len(node.children[ci+1].keys) > self._minkeys:
                    node.keys.append(node.children[ci+1].keys.pop(0))
                    node.children[ci].keys.append(node.keys.pop(0))
                    self.delete(node.children[ci], key)
                else:
                    if ci >= 1:
                        node.children[ci-1].keys.append(node.keys.pop(ci-1))
                        rnode = node.children.pop(ci)
                        node.children[ci-1].keys.extend(rnode.keys)
                        node.children[ci-1].children.extend(rnode.children)
                        if node == self.root and not node.keys:
                            self.root = node.children[ci-1]
                        self.delete(node.children[ci-1], key)
                    else:
                        node.children[ci].keys.append(node.keys.pop(ci))
                        rnode = node.children.pop(ci+1)
                        node.children[ci].keys.extend(rnode.keys)
                        node.children[ci].children.extend(rnode.children)
                        if node == self.root and not node.keys:
                            self.root = node.children[ci]
                        self.delete(node.children[ci], key)
            else:
                self.delete(node.children[ci], key)

    def levels(self):
        if self.root:
            level = 1
            leveldict = {1: [self.root]}
            while 1:
                maxlevel = False
                for node in leveldict.get(level):
                    if node.children:
                        for e in node.children:
                            leveldict.setdefault(level+1, []).append(e)
                    if node.isLeaf:
                        maxlevel = True
                if maxlevel:
                    break
                level += 1
            return leveldict
        else:
            return {}

    def breadth_first_traversal(self, node):
        q = Queue()
        q.put(node)
        
        while not q.empty():
            node = q.get()
            print node
            if node.left is not None :
                q.put(node.leftChild)
            if node.right is not None :
                q.put(node.rightChild)

    def __setitem__(self, k, v):
        pass

    def __getitem__(self, k, v):
        pass

    def __delitem__(self, k, v):
        pass


if __name__ == '__main__':
    from pprint import pprint
    b = BTree(2)
    b.insert(0)
    b.insert(8)
    b.insert(9)
    b.insert(1)
    b.insert(7)
    b.insert(2)
    b.insert(6)
    b.insert(3)
    b.insert(5)
    b.insert(4)
    b.delete(b.root, 4)
    b.delete(b.root, 5)
    b.delete(b.root, 3)
    b.delete(b.root, 6)
    b.delete(b.root, 2)
    b.delete(b.root, 7)
    b.delete(b.root, 1)
    b.delete(b.root, 9)
    pprint(b.levels())
    #n, i = b.search(b.root, 6)
    #print n, i
