#! /usr/bin/env python
# coding: utf-8

import Queue


class Node(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.data = {}
        self.is_same = False
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

    def calcsum(self):
        if self.is_same:
            return self.data.get('value', 0) * \
                   (self.end - self.start +1)
        else:
            #return self.data.get('sum', 0)
            return self.data.get('sum', 0) + \
                   self.data.get('delta', 0) * \
                   (self.end - self.start +1)

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
        return '[%s,%s]v:%s' % (self.start, self.end, self.data.get('value', 0))

    __repr__ = __str__

class SegmentTree(object):

    def __init__(self, points = []):
        self.points = sorted(points)
        self.root = self.build(self.points)

    def push_up(self, node):
        pass
    
    def push_down(self, node):
        pass

    def build(self, points):
        n = len(points)
        if n < 1:
            return None
        m = (n+1)/2
        node = Node(points[0], points[-1])
        if n > 1:
            node.left = self.init(points[:m])
            if node.left:
                node.left.parent = node
            node.right = self.init(points[m:])
            if node.right:
                node.right.parent = node

        return node

    def query(self, start, end, key = 'max'):
        """
        key: ['max', 'min', 'sum', 'delta']
        
        >>> st = SegmentTree(range(5))
        >>> st.query(2, 4)
        [[3,4], [3,3], [4,4]]
        >>> st.pprint() # doctest: +SKIP
        """
        return self._query(self.root, start, end, [])

    def _query(self, node, start, end, result = []):
        if node is None:
            return result
        if start <= node.start and node.end <= end:
            result.append(node)
        mid = (node.start + node.end)/2
        if start < mid:
            self._query(node.left, start, end, result)
        if end > mid:
            self._query(node.right, start, end, result)

        return result

    def query_sum(self, start, end):
        """
        Can we mix the set and add methods?
        
        >>> st = SegmentTree(range(4))
        >>> st.set(1, 3, 1)
        >>> st.add(1, 3, 1)
        >>> st.query_sum(1, 3)
        6
        >>> st.query_sum(2, 3)
        4
        >>> st.query_sum(0, 1)
        2
        >>> st.query_sum(0, 0)
        0
        >>> st.query_sum(1, 1)
        2
        >>> st.query_sum(2, 2)
        2
        >>> st.pprint()
        """
        return self._query_sum(self.root, start, end)

    def _query_sum(self, node, start, end):
        result = 0
        
        if node is None:
            return
            
        if start <= node.start and node.end <= end:
            if node.is_same:
                result += node.data.get('value', 0) * (node.end - node.start + 1)
            else:
                result += node.data.get('sum', 0) + \
                          node.data.get('delta', 0) * (node.end - node.start + 1)
        else:
            if node.is_same:
                if node.has_left():
                    node.left.data['value'] = node.data.get('value', 0)
                    node.left.is_same = True
                if node.has_right():
                    node.right.data['value'] = node.data.get('value', 0)
                    node.right.is_same = True
                node.is_same = False
            else:
                node.data['sum'] = node.data.get('sum', 0) + \
                                   node.data.get('delta', 0) * \
                                   (node.end - node.start + 1)
                node.left.data['delta'] = node.left.data.get('delta', 0) + \
                                          node.data.get('delta', 0)
                node.right.data['delta'] = node.right.data.get('delta', 0) + \
                                           node.data.get('delta', 0)
                node.data['delta'] = 0
            mid = (node.start + node.end)/2
            if start <= mid:
                result += self._query_sum(node.left, start, end)
            if end > mid:
                result += self._query_sum(node.right, start, end)
        
        return result

    def query_min(self, start, end):
        return self._query_min(self.root, start, end)
    
    def _query_min(self, node, start, end):
        pass
    
    def query_max(self, start, end):
        return self._query_max(self.root, start, end)

    def _query_max(self, node, start, end):
        result = 0
        if node is None:
            return
        if start <= node.start and node.end <= end:
            result = node.data.get('max', 0)
        else:
            delta = node.data.get('delta', 0)
            node.left.data['delta'] += delta
            node.right.data['delta'] += delta
            node.left.data['max'] += delta
            node.right.data['max'] += delta
            node.data['delta'] =  0
            mid = (node.start + node.end)/2
            if start <= mid:
                result = self._query_max(node.left, start, end) + delta
            if end > mid:
                tmp = self._query_max(node.right, start, end) + delta
                if result < tmp:
                    result = tmp
        
        return result

    def update_node(self, x, data = {}):
        """
        >>> st = SegmentTree(range(3))
        >>> st.update_node(1, {'max':2})
        >>> st.pprint() # doctest: +SKIP
                                                [0,2]:{'max': 2}
                               /                               \
                [0,1]:{'max': 2}                                [2,2]:{}
               /               \
        [0,0]:{}                [1,1]:{'max': 2}
        """
        self._update_node(self.root, x, data)
        
    def _update_node(self, node, x, data = {}):
        if node is None:
            return
        if node.is_leaf():
            node.data.update(data)
        else:
            mid = (node.start + node.end)/2
            if x <= mid:
                self._update_node(node.left, x, data)
            else:
                self._update_node(node.right, x, data)
            if 'sum' in data:
                node.data['sum'] = node.left.data.get('sum', 0) + node.right.data.get('sum', 0)
            if 'max' in data:
                node.data['max'] = max(
                    node.left.data.get('max', 0), node.right.data.get('max', 0)
                )
            if 'min' in data:
                node.data['min'] = min(
                    node.left.data.get('min', 0), node.right.data.get('min', 0)
                )

    def add(self, start, end, delta):
        """
        >>> st = SegmentTree(range(4))
        >>> st.add(1, 3, 2)
        >>> st.query_sum(1, 3)
        6
        >>> st.query_sum(2, 3)
        4
        >>> st.query_sum(0, 1)
        2
        >>> st.query_sum(0, 0)
        0
        >>> st.query_sum(1, 1)
        2
        >>> st.query_sum(2, 2)
        2
        >>> st.pprint() #doctest: +SKIP
                                [0,3]d:0
                       /                       \
                [0,1]d:0                        [2,3]d:2
               /       \                       /       \
        [0,0]d:0        [1,1]d:2        [2,2]d:0        [3,3]d:0
                                [0,3]s:6
                       /                       \
                [0,1]s:2                        [2,3]s:0
               /       \                       /       \
        [0,0]s:0        [1,1]s:0        [2,2]s:0        [3,3]s:0
        """
        self._add(self.root, start, end, delta)
        
    def _add(self, node, start, end, delta):
        if node is None:
            return
        if start <= node.start and node.end <= end:
            node.data['delta'] = node.data.setdefault('delta', 0) + delta
            node.data['max'] = node.data.setdefault('max', 0) + delta
        else:
            mid = (node.start + node.end)/2
            if start <= mid:
                self._add(node.left, start, end, delta)
            if end > mid:
                self._add(node.right, start, end, delta)
            node.data['max'] = node.data.get('delta', 0) + max(
                node.left.data.get('max', 0),
                node.right.data.get('max', 0)
            )
            node.data['sum'] = node.left.data.get('sum', 0) + \
                               node.left.data.get('delta', 0) * \
                               (node.left.end - node.left.start + 1)
            node.data['sum'] += node.right.data.get('sum', 0) + \
                                node.right.data.get('delta', 0) * \
                                (node.right.end - node.right.start + 1)

    def set(self, start, end, value):
        """
        >>> st = SegmentTree(range(4))
        >>> st.set(1, 3, 2)
        >>> st.query_sum(1, 3)
        6
        >>> st.query_sum(2, 3)
        4
        >>> st.query_sum(0, 1)
        2
        >>> st.query_sum(0, 0)
        0
        >>> st.query_sum(1, 1)
        2
        >>> st.query_sum(2, 2)
        2
        >>> st.pprint() # doctest: +SKIP
                                [0,3]v:0
                       /                       \
                [0,1]v:0                        [2,3]v:2
               /       \                       /       \
        [0,0]v:0        [1,1]v:2        [2,2]v:0        [3,3]v:0
        """
        self._set(self.root, start, end, value)
    
    def _set(self, node, start, end, value):
        if node is None:
            return
        if node.is_same:
            node.data['sum'] = node.data.get('value', 0) * \
                               (node.end - node.start + 1)
            if node.has_left():
                node.left.data['value'] = node.data.get('value', 0)
                node.left.is_same = True
            if node.has_right():
                node.right.data['value'] = node.data.get('value', 0)
                node.right.is_same = True
            node.is_same = False
        if start <= node.start and node.end <= end:
            node.is_same = True
            node.data['value'] = value
        else:
            mid = (node.start + node.end)/2
            if start <= mid:
                self._set(node.left, start, end, value)
            if end > mid:
                self._set(node.right, start, end, value)
            node.data['sum'] = node.left.calcsum() + node.right.calcsum()
        

    #### some common methods

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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
