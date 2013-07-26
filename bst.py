#! /usr/bin/env python
# coding: utf-8


import sys
from Queue import Queue


class TreeNode:
    
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self
    
    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent
    
    def findSuccessor(self):
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ
    
    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def __iter__(self):
       if self:
          if self.hasLeftChild():
              for elem in self.leftChiLd:
                  yield elem
          yield self.key
          if self.hasRightChild():
              for elem in self.rightChild:
                  yield elem

    def __str__(self):
        return '[k, v]: %s, %s' %(self.key, self.payload)

    def __str__(self):
        return '(%s) ' % self.key

    def __repr__(self):
        return '[k, v]: %s, %s' %(self.key, self.payload)


class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size += 1

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent = currentNode)
        elif key > currentNode.key:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent = currentNode)
        else:
            currentNode.payload = val

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif key == currentNode.key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def delete(self, key):
        if self.size > 1:
            node = self._get(key, self.root)
            if node:
                self.remove(node)
                self.size -= 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('Error, key not in tree')

    def remove(self,currentNode):
        if currentNode.isLeaf(): #leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren(): #interior
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload
        else: # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                       currentNode.leftChild.payload,
                                       currentNode.leftChild.leftChild,
                                       currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                       currentNode.rightChild.payload,
                                       currentNode.rightChild.leftChild,
                                       currentNode.rightChild.rightChild)

    def searchRange(self, kmin, kmax):
        result = []
        if self.root:
            self._searchRange(kmin, kmax, result, self.root)
        return result
    
    def _searchRange(self, kmin, kmax, result, currentNode):
        if currentNode:
            if  kmin < currentNode.key:
                self._searchRange(kmin, kmax, result, currentNode.leftChild)
            if kmin <= currentNode.key <= kmax:
                result.append(currentNode)
            if kmin > currentNode.key or currentNode.key < kmax:
                self._searchRange(kmin, kmax, result, currentNode.rightChild)

    def printLevelOrder(self):
        if not self.root:
            return
        currentLevel = Queue()
        nextLevel = Queue()
        currentLevel.put(self.root)
        while not currentLevel.empty():
            curNode = currentLevel.get()
            if curNode:
                sys.stdout.write('%s ' % curNode.key)
                nextLevel.put(curNode.leftChild)
                nextLevel.put(curNode.rightChild)
            if currentLevel.empty():
                sys.stdout.write('\n')
                currentLevel, nextLevel = nextLevel, currentLevel


    def splitLevels(self):
        if self.root:
            level = 1
            leveldict = {1: [self.root]}
            while 1:
                maxlevel = []
                for node in leveldict.get(level):
                    if node.leftChild != None:
                        leveldict.setdefault(level+1, []).append(node.leftChild)
                        maxlevel.append(False)
                    if node.rightChild != None:
                        leveldict.setdefault(level+1, []).append(node.rightChild)
                        maxlevel.append(False)
                    if node.isLeaf():
                        maxlevel.append(True)
                if all(maxlevel):
                    break
                level += 1
            return leveldict
        else:
            return {}

    def printTree(self):
        nodes = self.inorder()
        length = [len(str(e)) for e in nodes]
        leveldict = self.splitLevels()
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
                if node.isLeftChild():
                    branches.append((end-1, '/'))
                elif node.isRightChild():
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


    def preorder(self):
        return self._preorder(self.root)
    
    def _preorder(self, currentNode):
        nodes = []
        nodes.append(currentNode)
        if currentNode.hasLeftChild():
            nodes.extend(self._preorder(currentNode.leftChild))
        if currentNode.hasRightChild:
            nodes.extend(self._preorder(currentNode.rightChild))
        
        return nodes

    def inorder(self):
        return self._inorder(self.root)
    
    def _inorder(self, currentNode):
        nodes = []
        if currentNode.hasLeftChild():
            nodes.extend(self._inorder(currentNode.leftChild))
        nodes.append(currentNode)
        if currentNode.hasRightChild():
            nodes.extend(self._inorder(currentNode.rightChild))
        
        return nodes

    def postorder(self):
        return self._postorder(self.root)
    
    def _postorder(self, currentNode):
        nodes = []
        if currentNode.hasLeftChild():
            nodes.extend(self._postorder(currentNode.leftChild))
        nodes.append(currentNode)
        if currentNode.hasRightChild():
            nodes.extend(self._postorder(currentNode.rightChild))
        
        return nodes

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


if __name__ == '__main__':
    #test_BinaryTree()
    r = BinarySearchTree()
    r.put(6, 'root')
    r.put(3, 'left')
    r.put(9, 'right')
    r.put(5, 'where')
    r.put(2, 'two')
    min = r.root.findMin()
    print min.findSuccessor().isLeaf()
    print min.isLeaf()
    print r.root
    print r.root.findSuccessor()
    print r.get(9)
    r.delete(5)
    print min.findSuccessor()
    r.put(5, 'leaf')
    r.put(4, 'test')
    r.put(10, 'large')
    print min.findSuccessor()
    print 'search range:'
    result = r.searchRange(7, 9)
    print result
    print
    r.printLevelOrder()
    r.printTree()