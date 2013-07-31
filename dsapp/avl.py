#! /usr/bin/env python
#coding: utf-8

import sys
import random

MAXINT = 1000

class AVLNode(object):
    
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.balance = 0
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

    def findPrecursor(self):
        prec = None
        if self.hasLeftChild():
            prec = self.leftChild.findMax()
        else:
            if self.parent:
                if self.isRightChild():
                    prec = self.parent
                else:
                    self.parent.leftChild = None
                    self.parent.findPrecursor()
                    self.parent.leftChild = self

    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def findMax(self):
        current = self
        while current.hasRightChild():
            current = current.rightChild
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
        return '(%s:%s) ' % (self.key, self.balance)

    __repr__ = __str__


class AVLTree(object):

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size


    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = AVLNode(key, val)
        self.size += 1

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = AVLNode(key, val, parent = currentNode)
                self.updateBalance(currentNode.leftChild)
        elif key > currentNode.key:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = AVLNode(key, val, parent = currentNode)
                self.updateBalance(currentNode.rightChild)

    def updateBalance(self, node):
        if node.balance < -1 or node.balance > 1:
            self.rebalance(node)
            return
        if node.parent != None:
            if node.isLeftChild():
                node.parent.balance += 1
            elif node.isRightChild():
                node.parent.balance -= 1
            if node.parent.balance != 0:
                self.updateBalance(node.parent)

    def rebalance(self, node):
        if node.balance < 0:
            if node.rightChild.balance > 0:
                self.rightRotate(node.rightChild)
                self.leftRotate(node)
            else:
                self.leftRotate(node)
        elif node.balance > 0:
            #print node
            if node.leftChild.balance < 0:
                self.leftRotate(node.leftChild)
                self.rightRotate(node)
            else:
                self.rightRotate(node)

    def leftRotate(self, currentNode):
        """From bottom to up."""
        node = currentNode.rightChild
        currentNode.rightChild = node.leftChild
        if node.leftChild != None:
            node.leftChild.parent = currentNode
        node.parent = currentNode.parent
        if currentNode.isRoot():
            self.root = node
        else:
            if currentNode.isLeftChild():
                currentNode.parent.leftChild = node
            else:
                currentNode.parent.rightChild = node
        node.leftChild = currentNode
        currentNode.parent = node
        currentNode.balance = currentNode.balance + 1 - min(node.balance, 0)
        node.balance = node.balance + 1 + max(currentNode.balance, 0) 


    def rightRotate(self, currentNode):
        """From bottom to up."""
        node = currentNode.leftChild
        currentNode.leftChild = node.rightChild
        if node.rightChild != None:
            node.rightChild.parent = currentNode
        node.parent = currentNode.parent
        if currentNode.isRoot():
            self.root = node
        else:
            if currentNode.isLeftChild():
                currentNode.parent.leftChild = node
            else:
                currentNode.parent.rightChild = node
        node.rightChild = currentNode
        currentNode.parent = node
        currentNode.balance = currentNode.balance - 1 - max(node.balance, 0)
        node.balance = node.balance - 1 + min(currentNode.balance, 0) 

    
    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res
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
            if currentNode.balance > 0:
                self.rightRotate(currentNode)
            else:
                self.leftRotate(currentNode)
            self.remove(currentNode)
        else:
            if currentNode.hasLeftChild():
                currentNode.parent.leftChild = currentNode.leftChild
                currentNode.leftChild.parent = currentNode.parent
            if currentNode.hasRightChild():
                currentNode.parent.rightChild = currentNode.rightChild
                currentNode.rightChild.parent = currentNode.parent

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
    r = AVLTree()
    r.put(1, 'first')
    r.put(2, 'two')
    r.put(3, 'third')
    r.put(4, 'four')
    r.put(5, 'five')
    r.put(6, 'six')
    r.put(7, 'seven')
    r.put(8, 'eight')
    r.put(9, 'nine')
    r.put(10, 'ten')
    r.put(11, 'elenve')
    #r.printTree()
    r.delete(r.root.key)
    #r.put(5, 'five')

    print 'AVL size: ', r.size
    r.printTree()
    print r.searchRange(3, 7)
