#! /usr/bin/env python
# coding: utf-8


class BinaryNodeBase(object):
    
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None

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
        return '[%s,%s]' % (self.start, self.end)

    __repr__ = __str__


class BinaryTreeBase(object)

    def preorder(self):
        return self._preorder(self.root)

    def _preorder(self, node):
        nodes = []
        nodes.append(node)
        if node.has_left():
            nodes.extend(self._preorder(node.left))
        if node.has_right():
            nodes.extend(self._preorder(node.right))

        return nodes

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

    def postorder(self):
        return self._postorder(self.root)

    def _postorder(self, node):
        nodes = []
        if node.has_left():
            nodes.extend(self._postorder(node.left))
        if node.has_right():
            nodes.extend(self._postorder(node.right))
        nodes.append(node)

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

