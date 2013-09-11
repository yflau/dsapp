#! /usr/bin/env python
# coding: utf-8

"""

Leftest tree.

Reference:

- http://wenku.baidu.com/view/20e9ff18964bcf84b9d57ba1.html

"""

import Queue
from collections import deque


def merge(A, B):
    if not A:
        return B
    if not B:
        return A
        
    if B.key < A.key:
        tmp = A
        A = B
        B = tmp
    
    A.right = merge(A.right, B)
    A.right.parent = A
    if getattr(A.right, 'dist', -1) > getattr(A.left, 'dist', -1):
        tmp = A.left
        A.left = A.right
        A.right = tmp
    
    if A.right is None:
        A.dist = 0
    else:
        A.dist = A.right.dist + 1
        
    return A


class LeftistNode(object):
    
    def __init__(self, key, value = None):
        self.key = key
        self.value = value
        self.dist = 0
        self.left = None
        self.right = None
        self.parent = None

    def is_external(self):
        return (self.left and not self.right) or (not self.left and self.right)

    def merge(self, B):
        return merge(self, B)

    ### methods should be inherited from BaseNode class
    def has_left(self):
        return self.left

    def has_right(self):
        return self.right

    def is_left(self):
        return self.parent and self.parent.left == self

    def is_right(self):
        return self.parent and self.parent.right == self

    def is_root(self):
        return not self.parent

    def is_leaf(self):
        return not (self.right or self.left)

    def has_any_children(self):
        return self.right or self.left

    def has_both_children(self):
        return self.right and self.left

    @property
    def depth(self):
        """depth of node, root is 0."""
        depth = 0
        parent = self.parent

        while parent is not None:
            depth += 1
            parent = parent.parent

        return depth

    def __str__(self):
        return '(%s:%s)' % (self.key, self.dist)

    __repr__ = __str__


class LeftistTree(object):
    
    def __init__(self):
        self.root = None
    
    def build(self, q):
        """
        >>> t =LeftistTree()
        >>> t.build([(1,), (2,), (3,), (4,), (5,), (6,)])
        >>> t.pprint() # doctest: +SKIP
                            (1:1)
                 /              \
             (3:1)               (2:0)
            /         \
        (4:0)          (5:0)
                      /
                  (6:0)
        """
        q = [LeftistNode(*e) for e in q]
        q = deque(q)
        
        while len(q) > 1:
            a = q.popleft()
            b = q.popleft()
            q.append(a.merge(b))
            
        if len(q) == 1:
            self.root = q[0]
    
    def merge(self, T):
        """
        >>> t1 =LeftistTree()
        >>> kvs = [(1,), (99,), (25,), (7,), (20,), (50,), (5,), (10,), (15,)]
        >>> t1.build(kvs)
        >>> t1.pprint() # doctest: +SKIP
                         (1:2)
                  /                            \
              (5:1)                             (7:1)
             /    \                      /          \
        (10:0)     (15:0)           (20:1)           (25:0)
                                   /     \
                              (50:0)      (99:0)
        >>> t2 =LeftistTree()
        >>> kvs = [(22,), (75,)]
        >>> t2.build(kvs)
        >>> t2.pprint() # doctest: +SKIP
              (22:0)
             /
        (75:0)
        >>> t1.merge(t2)
        >>> t1.pprint() # doctest: +SKIP
                                                 (1:2)
                              /                            \
                          (7:2)                             (5:1)
                   /                \                      /    \
              (20:1)                 (22:1)           (10:0)     (15:0)
             /     \                /     \
        (50:0)      (99:0)     (75:0)      (25:0)
        """
        self.root = self.root.merge(T.root)
        
    def insert(self, x):
        """
        >>> t =LeftistTree()
        >>> kvs = [(1,), (99,), (25,), (7,), (20,), (50,), (5,), (10,), (15,)]
        >>> t.build(kvs)
        >>> t.pprint() # doctest: +SKIP
                         (1:2)
                  /                            \
              (5:1)                             (7:1)
             /    \                      /          \
        (10:0)     (15:0)           (20:1)           (25:0)
                                   /     \
                              (50:0)      (99:0)
        >>> t.insert(LeftistNode(6))
        >>> t.pprint()  # doctest: +SKIP
                         (1:1)
                  /                                       \
              (5:1)                                        (6:0)
             /    \                                 /
        (10:0)     (15:0)                       (7:1)
                                         /          \
                                    (20:1)           (25:0)
                                   /     \
                              (50:0)      (99:0)
        """
        self.root = self.root.merge(x)
    
    def pop(self):
        """
        >>> t =LeftistTree()
        >>> kvs = [(1,), (99,), (25,), (7,), (20,), (50,), (5,), (10,), (15,)]
        >>> t.build(kvs)
        >>> t.pprint() # doctest: +SKIP
                         (1:2)
                  /                            \
              (5:1)                             (7:1)
             /    \                      /          \
        (10:0)     (15:0)           (20:1)           (25:0)
                                   /     \
                              (50:0)      (99:0)
        >>> t.pop()
        1
        >>> t.pprint() # doctest: +SKIP
                                           (5:1)
                              /                \
                          (7:1)                 (10:0)
                   /                \
              (20:1)                 (15:0)
             /     \                /
        (50:0)      (99:0)     (25:0)
        """
        t = self.root.key
        self.root = self.root.left.merge(self.root.right)

        return t
        
    def delete(self, x):
        pass

    ### methods should inherited from BaseTree class
    def inorder(self):
        return self._inorder(self.root)

    def _inorder(self, node):
        nodes = []
        if node.has_left():
            nodes.extend(self._inorder(node.left))
        nodes.append(node)
        if node.has_right():
            nodes.extend(self._inorder(node.right))

        return nodes

    def bft(self, node, level = 1):
        """Breadth first traversal."""
        q = Queue.Queue()
        level = level
        q.put((level, node))

        while not q.empty():
            level, node = q.get()
            yield (level, node)
            if node.has_left():
                q.put((level+1, node.left))
            if node.has_right():
                q.put((level+1, node.right))
                
    def levels(self):
        leveldict = {}

        for level, node in self.bft(self.root):
            leveldict.setdefault(level, []).append(node)

        return leveldict

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
                if node.is_left():
                    branches.append((end-1, '/'))
                elif node.is_right():
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
    import doctest
    doctest.testmod()
