#! /usr/bin/env python
#coding: utf-8


class SBTNode(object):
    
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.value = val
        self.size = 1
        self.left = left
        self.right = right
        self.parent = parent

    def hasLeft(self):
        return self.left

    def hasRight(self):
        return self.right

    def isLeft(self):
        return self.parent and self.parent.left == self

    def isRight(self):
        return self.parent and self.parent.right == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.right or self.left)

    def hasAnyChildren(self):
        return self.right or self.left

    def hasBothChildren(self):
        return self.right and self.left

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.value = value
        self.left = lc
        self.right = rc
        if self.hasLeft():
            self.left.parent = self
        if self.hasRight():
            self.right.parent = self

    def successor(self):
        succ = None
        if self.hasRight():
            succ = self.right.findMin()
        else:
            if self.parent:
                if self.isLeft():
                    succ = self.parent
                else:
                    self.parent.right = None
                    succ = self.parent.successor()
                    self.parent.right = self
        return succ

    def precursor(self):
        prec = None
        if self.hasLeft():
            prec = self.left.findMax()
        else:
            if self.parent:
                if self.isRight():
                    prec = self.parent
                else:
                    self.parent.left = None
                    self.parent.precursor()
                    self.parent.left = self

    def findMin(self):
        current = self
        while current.hasLeft():
            current = current.left
        return current

    def findMax(self):
        current = self
        while current.hasRight():
            current = current.right
        return current

    def __iter__(self):
       if self:
          if self.hasLeft():
              for elem in self.left:
                  yield elem
          yield self.key
          if self.hasRight():
              for elem in self.right:
                  yield elem

    def __str__(self):
        return '(%s:%s) ' % (self.key, self.size)

    __repr__ = __str__


class SBTree(object):

    def __init__(self):
        self.root = None
        self.size = 0
        self.record = None

    # standard methods
    
    def leftRotate(self, t):
        """From bottom to up."""
        node = t.right
        t.right = node.left
        if node.left != None:
            node.left.parent = t
        node.parent = t.parent
        if t.isRoot():
            self.root = node
        else:
            if t.isLeft():
                t.parent.left = node
            else:
                t.parent.right = node
        node.size = t.size
        if t.left:
            lsize = t.left.size
        else:
            lsize = 0
        if t.right:
            rsize = t.right.size
        else:
            rsize = 0
        t.size = lsize + rsize + 1
        node.left = t
        t.parent = node

    def rightRotate(self, t):
        """From bottom to up."""
        node = t.left
        t.left = node.right
        if node.right != None:
            node.right.parent = t
        node.parent = t.parent
        
        if t.isRoot():
            self.root = node
        else:
            if t.isLeft():
                t.parent.left = node
            else:
                t.parent.right = node
        node.size = t.size
        if t.left:
            lsize = t.left.size
        else:
            lsize = 0
        if t.right:
            rsize = t.right.size
        else:
            rsize = 0
        t.size = lsize + rsize + 1
        node.right = t
        t.parent = node
        
    def maintain(self, t, flag):
        if not t:
            return
            
        if flag == False:
            if t.right:
                usize = t.right.size
            else:
                usize = 0
            if t.left:
                if t.left.hasLeft():
                    if t.left.left.size > usize:
                        self.rightRotate(t)
                    else:
                        return
                else:
                    if t.left.hasRight():
                        if t.left.right.size > usize:
                            self.leftRotate(t.left)
                            self.rightRotate(t)
                        else:
                            return
                    else:
                        return
            else:
                return
        else:
            if t.left:
                usize = t.left.size
            else:
                usize = 0
            if t.right:
                if t.right.hasRight():
                    if t.right.right.size > usize:
                        self.leftRotate(t)
                    else:
                        return
                else:
                    if t.right.hasLeft():
                        if t.right.left.size > usize:
                            self.rightRotate(t.right)
                            self.leftRotate(t)
                        else:
                            return
                    else:
                        return
            else:
                return
                
        self.maintain(t.left, False)
        self.maintain(t.right, True)
        self.maintain(t, False)
        self.maintain(t, True)

    def insert(self, key, val):
        if self.root:
            self._insert(key, val, self.root)
        else:
            self.root = SBTNode(key, val)
        self.size += 1

    def _insert(self, key, val, t):
        t.size += 1
        if key < t.key:
            if t.hasLeft():
                self._insert(key, val, t.left)
            else:
                t.left = SBTNode(key, val, parent = t)
        elif key > t.key:
            if t.hasRight():
                self._insert(key, val, t.right)
            else:
                t.right = SBTNode(key, val, parent = t)
        self.maintain(t, key >= t.key)

    def find(self, key):
        if self.root:
            res = self._find(key, self.root)
            if res:
                return res
            else:
                return None
        else:
            return None

    def _find(self, key, t):
        if not t:
            return None
        elif key == t.key:
            return t
        elif key < t.key:
            return self._find(key, t.left)
        else:
            return self._find(key, t.right)

    def delete(self, key, type = 'faster_and_simpler'):
        """Delete method of SBT.
        
        type: 
          standard : standard delete
          faster_and_simpler : faster and simpler delete, default
        """
        if self.size > 1:
            remove = getattr(self, '_%s_remove' % type, 'faster_and_simpler_remove')
            remove(self.root, key)
            self.size -= 1
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('Error, key not in tree')

    def _standard_remove(self, t, key):
        if t.size <= 2:
            self.record = t
            if t.isLeaf(): #leaf
                if t == t.parent.left:
                    t.parent.left = None
                else:
                    t.parent.right = None
            else:
                if t.hasLeft():
                    t.parent.left = t.left
                    t.left.parent = t.parent
                if t.hasRight():
                    t.parent.right = t.right
                    t.right.parent = t.parent
            return
        t.size -= 1
        if key == t.key:
            self._standard_remove(t.left, key+1)
            t.key = self.record.key
            t.value = self.record.value
            self.maintain(t, True)
        else:
            if key < t.key:
                self._standard_remove(t.left, key)
            else:
                self._standard_remove(t.right, key)
            self.maintain(t, key < t.key)

    def _faster_and_simpler_remove(self, t, key):
        t.size -= 1
        self.record = t
        k = t.key
        if key == k or (key < k and not t.hasLeft()) or (key > k and not t.hasRight()):
            if t.isLeaf(): #leaf
                if t == t.parent.left:
                    t.parent.left = None
                else:
                    t.parent.right = None
            elif t.hasBothChildren(): #interior
                self._faster_and_simpler_remove(t.left, key+1)
                t.key = self.record.key
                t.value = self.record.value
            else:
                if t.hasLeft():
                    t.parent.left = t.left
                    t.left.parent = t.parent
                if t.hasRight():
                    t.parent.right = t.right
                    t.right.parent = t.parent
        else:
            if key < k:
                self.faster_and_simpler_remove(t.left, key)
            else:
                self.faster_and_simpler_remove(t.right, key)
            
    def select(self, t, k):
        if not t or k > t.size:
            return None
        r = (0 if not t.hasLeft() else t.left.size)+1
        if k == r:
            return t
        elif k < r:
            return self.select(t.left, k)
        else:
            return self.select(t.right, k-r)
    
    def rank(self, t, v):
        if not t:
            return 0
        if v == t.key:
            return (0 if not t.hasLeft() else t.left.size) + 1
        elif v < t.key:
            return self.rank(t.left, v)
        else:
            r = self.rank(t.right, v)
            tmp = (0 if not t.hasLeft() else t.left.size)
            return 0 if r == 0 else (r + tmp + 1)

    # override operators
    def __getitem__(self, k):
        return self.get(k)

    def __contains__(self, k):
        if self._get(k, self.root):
            return True
        else:
            return False

    def __setitem__(self, k, v):
        self.put(k, v)

    def __delitem__(self, key):
        self.delete(key)

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    # Additional methods
    put = insert
    get = find
    
    def length(self):
        return self.size
        
    def preorder(self):
        return self._preorder(self.root)
    
    def _preorder(self, t):
        nodes = []
        nodes.append(t)
        if t.hasLeft():
            nodes.extend(self._preorder(t.left))
        if t.hasRight:
            nodes.extend(self._preorder(t.right))
        
        return nodes

    def inorder(self):
        return self._inorder(self.root)
    
    def _inorder(self, t):
        nodes = []
        if t.hasLeft():
            nodes.extend(self._inorder(t.left))
        nodes.append(t)
        if t.hasRight():
            nodes.extend(self._inorder(t.right))
        
        return nodes

    def postorder(self):
        return self._postorder(self.root)
    
    def _postorder(self, t):
        nodes = []
        if t.hasLeft():
            nodes.extend(self._postorder(t.left))
        nodes.append(t)
        if t.hasRight():
            nodes.extend(self._postorder(t.right))
        
        return nodes
    
    def searchRange(self, kmin, kmax):
        result = []
        if self.root:
            self._searchRange(kmin, kmax, result, self.root)
        return result
    
    def _searchRange(self, kmin, kmax, result, t):
        if t:
            if  kmin < t.key:
                self._searchRange(kmin, kmax, result, t.left)
            if kmin <= t.key <= kmax:
                result.append(t)
            if kmin > t.key or t.key < kmax:
                self._searchRange(kmin, kmax, result, t.right)

    def levels(self):
        if self.root:
            level = 1
            leveldict = {1: [self.root]}
            while 1:
                maxlevel = []
                for node in leveldict.get(level):
                    if node.left != None:
                        leveldict.setdefault(level+1, []).append(node.left)
                        maxlevel.append(False)
                    if node.right != None:
                        leveldict.setdefault(level+1, []).append(node.right)
                        maxlevel.append(False)
                    if node.isLeaf():
                        maxlevel.append(True)
                if all(maxlevel):
                    break
                level += 1
            return leveldict
        else:
            return {}

    def pprint(self):
        nodes = self.inorder()
        length = [len(str(e)) for e in nodes]
        leveldict = self.levels()
        levels = leveldict.keys()
        for level in levels:
            levelnodes = leveldict.get(level)
            starts = []
            ends = []
            branches = []
            for node in levelnodes:
                index = nodes.index(node)
                start = sum([len(str(e)) for e in nodes[:index]])
                end = start + len(str(node))
                starts.append(start)
                ends.append(end)
                if node.isLeft():
                    branches.append((end-1, '/'))
                elif node.isRight():
                    branches.append((start-1, '\\'))
                else:
                    if level > 1:
                        print 'error node: ', node
            if level > 1:
                spaces = [branches[0][0]]
                spaces.extend([branches[k+1][0] - branches[k][0] - 1 for k in range(len(branches)-1)])
                pair = ['%s%s' % (' '*spaces[m], branches[m][1]) for m in range(len(branches))]
                print ''.join(pair)
            spaces = [starts[0]]
            spaces.extend([starts[i] - ends[i-1] for i in range(1, len(starts))])
            pair = ['%s%s' % (' '*spaces[j], levelnodes[j]) for j in range(len(spaces))]
            print ''.join(pair)


if __name__ == '__main__':
    #test_BinaryTree()
    r = SBTree()
    r.insert(1, 'first')
    r.insert(2, 'two')
    r.insert(3, 'third')
    r.insert(4, 'four')
    r.insert(5, 'five')
    r.insert(6, 'six')
    r.insert(7, 'seven')
    r.insert(8, 'eight')
    r.insert(9, 'nine')
    r.insert(10, 'ten')
    r.insert(11, 'elenve')
    r.insert(12, 'twelve')
    r.pprint()
    #r.delete(r.root.key)
    #print r.root.key
    #print r.root.value
    r.delete(10, 'standard')
    r.insert(13, 'thirteen')
    print 'select: ', r.select(r.root, 12)
    print 'rank: ', r.rank(r.root, 13)

    print 'SBT size: ', r.size
    r.pprint()
    print r.searchRange(3, 7)
