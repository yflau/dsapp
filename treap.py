#! /usr/bin/env python
#coding: utf-8

import sys
import random

class TreapNode(object):
    
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.priority = random.randint(0, sys.maxint)
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
        return '[k, v]: %s, %s' %(self.key, self.payload)

    def __repr__(self):
        return '[k, v]: %s, %s' %(self.key, self.payload)


class Treap(object):

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size


    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreapNode(key, val)
        self.size += 1

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreapNode(key, val, parent = currentNode)
                if currentNode.leftChild.priority < currentNode.priority:
                    self.leftRotate(currentNode)
        elif key > currentNode.key:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreapNode(key, val, parent = currentNode)
                if currentNode.rightChild < currentNode.priority:
                    self.rightRotate(currentNode)
        else:
            currentNode.payload = val
            #currentNode.priority = random.randint(0, sys.maxint)


    def leftRotate(self, currentNode):
        """From bottom to up."""
        node = currentNode.rightChild
        currentNode.rightChild = node.leftChild
        node.leftChild = currentNode
        currentNode = node

    def rightRotate(self, currentNode):
        """From bottom to up."""
        node = currentNode.leftChild
        currentNode.leftChild = node.rightChild
        node.rightChild = currentNode
        currentNode = node
    
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
            if currentNode.leftChild.priority < currentNode.rightChild.priority:
                self.rightRotate(currentNode)
            else:
                self.leftRotate(currentNode)
            self.delete(key)
        elif:
            if currentNode.hasLeftChild():
                currentNode.parent.leftChild = currentNode.leftChild
                currentNode.leftChild.parent = currentNode.parent
            if currentNode.hasRightChild():
                currentNode.parent.rightChild = currentNode.rightChild
                currentNode.rightChild.parent = currentNode.parent
