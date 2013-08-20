#! /usr/bin/env python
# coding: utf-8

# based on chapter 20 of Introduction to Algorithms(Second Edition)

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
        x.keys.insert(i+1, y.keys[self.order-1])
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

    def delete(self, key):
        pass

    def __setitem__(self, k, v):
        pass

    def __getitem__(self, k, v):
        pass

    def __delitem__(self, k, v):
        pass

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


if __name__ == '__main__':
    from pprint import pprint
    b = BTree()
    b.insert(1)
    b.insert(3)
    b.insert(5)
    b.insert(2)
    b.insert(4)
    b.insert(6)
    b.insert(7)
    b.insert(9)
    b.insert(8)
    b.insert(10)
    b.insert(11)
    b.insert(12)
    b.insert(13)
    b.insert(14)
    b.insert(15)
    b.insert(16)
    b.insert(17)
    b.insert(18)
    b.insert(19)
    b.insert(20)
    b.insert(21)
    pprint(b.levels())
    n, i = b.search(b.root, 6)
    print n, i
