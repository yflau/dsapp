#! /usr/bin/env 
# coding: utf-8

"""http://stackoverflow.com/questions/9245151/size-balanced-binary-tree-heap-in-python"""

import random

class TreeNode( object ):
    """
       A (non-empty) binary tree node for a size-balanced binary tree heap.
       SLOTS:
         key: Orderable
         value: Any
         size: NatNum; the size of the sub-tree rooted at this node
         parent: NoneType|TreeNode; the parent node
         lchild: NoneType|TreeNode; the node of the left sub-tree
         rchild: NoneType|TreeNode; the node of the right sub-tree
    """
    __slots__ = ( 'key', 'value', 'size', 'parent', 'lchild', 'rchild' )

    def __init__( self, key, value, parent ):
        self.key = key
        self.value = value
        self.size = 1
        self.parent = parent
        self.lchild = None
        self.rchild = None

    def __str__( self ):
        slchild = str(self.lchild)
        srchild = str(self.rchild)
        skv = str((self.key, self.value)) + " <" + str(self.size) + ">"
        pad = " " * (len(skv) + 1)
        s = ""
        for l in str(self.lchild).split('\n'):
            s += pad + l + "\n"
        s += skv + "\n"
        for l in str(self.rchild).split('\n'):
            s += pad + l + "\n"
        return s[:-1]

class SBBTreeHeap( object ):
    """
       A size-balanced binary tree heap.
       SLOTS:
         root: NoneType|TreeNode
    """
    __slots__ = ( 'root' )

    def __init__( self ):
        self.root = None

    def __str__( self ):
        return str(self.root)

def checkNode( node, parent ):
    """
       checkNode: NoneType|TreeNode NoneType|TreeNode -> Tuple(NatNum, Boolean, Boolean, Boolean, Boolean)
       Checks that the node correctly records size information,
       correctly records parent information, satisfies the
       size-balanced property, and satisfies the heap property.
    """
    if node == None:
        return 0, True, True, True, True
    else:
        lsize, lsizeOk, lparentOk, lbalanceProp, lheapProp = checkNode( node.lchild, node )
        rsize, rsizeOk, rparentOk, rbalanceProp, rheapProp = checkNode( node.rchild, node )
        nsize = lsize + 1 + rsize
        nsizeOk = node.size == nsize
        sizeOk = lsizeOk and rsizeOk and nsizeOk
        nparentOk = node.parent == parent
        parentOk = lparentOk and rparentOk and nparentOk
        nbalanceProp = abs(lsize - rsize) <= 1
        balanceProp = lbalanceProp and rbalanceProp and nbalanceProp
        nheapProp = True
        if (node.lchild != None) and (node.lchild.key < node.key):
            nheapProp = False
        if (node.rchild != None) and (node.rchild.key < node.key):
            nheapProp = False
        heapProp = lheapProp and rheapProp and nheapProp
        return nsize, sizeOk, parentOk, balanceProp, heapProp

def checkHeap( heap ):
    """
       checkHeap: SBBTreeHeap -> NoneType
       Checks that the heap is a size-balanced binary tree heap.
    """
    __, sizeOk, parentOk, balanceProp, heapProp = checkNode( heap.root, None )
    if not sizeOk:
        print("** ERROR **  Heap nodes do not correctly record size information.")
    if not parentOk:
        print("** ERROR **  Heap nodes do not correctly record parent information.")
    if not balanceProp:
        print("** Error **  Heap does not satisfy size-balanced property.")
    if not heapProp:
        print("** Error **  Heap does not satisfy heap property.")
    assert(sizeOk and parentOk and balanceProp and heapProp)
    return


def empty(heap):
    """
       empty: SBBTreeHeap -> Boolean
       Returns True if the heap is empty and False if the heap is non-empty.
       Raises TypeError if heap is not an instance of SBBTreeHeap.
       Must be an O(1) operation.
    """

    if not SBBTreeHeap:
        print("** Error **  Heap is not an instance of SBBTreeHeap.")
    if heap.root == None:
        return True
    else:
        return False

def enqueue( heap, key, value ):
    """
       enqueue: SBBTreeHeap Orderable Any -> NoneType
       Adds the key/value pair to the heap.
       Raises TypeError if heap is not an instance of SBBTreeHeap.
       Must be an O(log n) operation.
    """
#    print('heap has entered enqueue')
#    print(str(heap))
    if empty(heap):
        heap.root = TreeNode(key, value, None)
    if heap.root.size < 3:
        if heap.root.lchild != None:
            if heap.root.rchild == None:
                heap.root.rchild = TreeNode(key, value, heap.root)
                heap.root.size += 1
        elif heap.root.lchild == None:
            heap.root.lchild = TreeNode(key, value, heap.root)
            heap.root.size += 1
    else:
        if heap.lchild.size >= heap.rchild.size:
            heap.lchild = TreeNode(key, value, heap.root)
        else:
            heap.rchild = TreeNode(key, value, heap.root)





def frontMin( heap ):
    """
       frontMin: SBBTreeHeap -> Tuple(Orderable, Any)
       Returns (and does not remove) the minimum key/value in the heap.
       Raises TypeError if heap is not an instance of SBBTreeHeap.
       Raises IndexError if heap is empty.
       Precondition: not empty(heap)
       Must be an O(1) operation.
    """
    ## COMPLETE frontMin FUNCTION ##


def dequeueMin( heap ):
    """
       dequeueMin: SBBTreeHeap -> NoneType
       Removes (and does not return) the minimum key/value in the heap.
       Raises TypeError if heap is not an instance of SBBTreeHeap.
       Raises IndexError if heap is empty.
       Precondition: not empty(heap)
       Must be an O(log n) operation.
    """
    ## COMPLETE dequeueMin FUNCTION ##


def heapsort( l ):
    """
       heapsort: ListOfOrderable -> ListOfOrderable
       Returns a list that has the same elements as l, but in ascending order.
       The implementation must a size-balanced binary tree heap to sort the elements.
       Must be an O(n log n) operation.
    """
    ## COMPLETE heapsort FUNCTION ##


######################################################################
######################################################################

if __name__ == "__main__":
#    R = random.Random()
#    R.seed(0)
#    print(">>> h = SBBTreeHeap()");
#    h = SBBTreeHeap()
#    print(h)
#    checkHeap(h)
#    for v in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#        k = R.randint(0,99)
#        print(">>> enqueue(h," + str(k) + "," + str(v) + ")")
#        enqueue(h, k, v)
#        print(h)
#        checkHeap(h)
#    while not empty(h):
#        print(">>> k, v = frontMin(h)")
#        k, v = frontMin(h)
#        print((k, v))
#        print(">>> dequeueMin(h)")
#        dequeueMin(h)
#        print(h)
#        checkHeap(h)
#    for i in range(4):
#        l = []
#        for x in range(2 ** (i + 2)):
#            l.append(R.randint(0,99))
#        print(" l = " + str(l))
#        sl = heapsort(l)
#        print("sl = " + str(sl))
#
#heap = SBBTreeHeap()
#print(empty(heap))

    R = random.Random()
    R.seed(0)
    print(">>> h = SBBTreeHeap()");
    h = SBBTreeHeap()
    print(h)
    checkHeap(h)
    for v in 'ABCDEFG':
        k = R.randint(0,99)
        print(">>> enqueue(h," + str(k) + "," + str(v) + ")")
        enqueue(h, k, v)
        print(h)
        checkHeap(h)