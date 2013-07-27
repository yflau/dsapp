#! /usr/bin/env python
# coding: utf-8

################################################################################

class BinaryTree(object):
    
    def __init__(self, root):
        self.root = root
        self.leftChild = None
        self.rightChild = None
    
    def getLeftChild(self):
        return self.leftChild
    
    def getRightChild(self):
        return self.rightChild

    def setRootVal(self, val):
        self.root = val

    def getRootVal(self):
        return self.root
    
    def insertLeft(self, val):
        if self.leftChild == None:
            self.leftChild = BinaryTree(val)
        else:
            t = BinaryTree(val)
            t.leftChild = self.leftChild
            self.leftChild = t
    
    def insertRight(self, val):
        if self.rightChild == None:
            self.rightChild = BinaryTree(val)
        else:
            t = BinaryTree(val)
            t.rightChild = self.rightChild
            self.rightChild = t

    def preorder(self):
        print self.root
        if self.leftChild:
            self.leftChild.preorder()
        if self.rightChild:
            self.rightChild.preorder()

    def inorder(self):
        if self.leftChild:
            self.leftChild.inorder()
        print self.root
        if self.rightChild:
            self.rightChild.inorder()

    def postorder(self):
        if self.leftChild:
            self.leftChild.postorder()
        if self.rightChild:
            self.rightChild.postorder()
        print self.root


def test_BinaryTree():
    r = BinaryTree('a')
    r.getRootVal()
    print(r.getLeftChild())
    r.insertLeft('b')
    print(r.getLeftChild())
    print(r.getLeftChild().getRootVal())
    r.insertRight('c')
    print(r.getRightChild())
    print(r.getRightChild().getRootVal())
    r.getRightChild().setRootVal('hello')
    print(r.getRightChild().getRootVal())
    r.getLeftChild().insertRight('e')
    
    print '\npreorder:'
    r.preorder()
    print '\ninorder:'
    r.inorder()
    print '\npostorder:'
    r.postorder()
