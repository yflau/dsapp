#! /usr/bin/env python
# coding: utf-8


"""
Segment tree and some examples.

Reference:
    
- http://www.notonlysuccess.com/index.php/segment-tree-complete/
- http://wenku.baidu.com/view/e55eb4a48762caaedd33d4fc.html

"""


import random
import Queue
from os.path import join
from io import BytesIO

from settings import DATA_PATH

################################################################################

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
        return '[%s,%s]' % (self.start, self.end)

    __repr__ = __str__

class SegmentTree(object):

    def __init__(self, points = []):
        self.points = sorted(points)
        self.root = self.build(self.points)

    def push_up(self, node):
        pass
    
    def _push_up_single_add(self, x, node = None):
        pass
    
    def _push_up_single_set(self, x, node = None):
        pass
    
    def _push_up_interval_add(self, start, end, node = None):
        pass
    
    def _push_up_interval_set(self, start, end, node = None):
        pass
    
    def push_down(self, node):
        pass

    def _push_down_single_add(self, x, node = None):
        pass

    def _push_down_single_set(self, x, node = None):
        pass
    
    def _push_down_interval_add(self, start, end, node = None):
        pass

    def _push_down_interval_set(self, start, end, node = None):
        pass

    def query(self, start, end):
        pass
    
    def update(self, start, end):
        pass

    def build(self, points):
        n = len(points)
        if n < 1:
            return None
        m = (n+1)/2
        node = Node(points[0], points[-1])
        if n > 1:
            node.left = self.build(points[:m])
            if node.left:
                node.left.parent = node
            node.right = self.build(points[m:])
            if node.right:
                node.right.parent = node
        self.push_up(node)

        return node

    def query_intersect(self, start, end, key = 'max'):
        """
        key: ['max', 'min', 'sum', 'delta']
        
        >>> st = SegmentTree(range(5))
        >>> st.query_intersect(2, 4)
        [[3,4], [3,3], [4,4]]
        >>> st.pprint() # doctest: +SKIP
        """
        return self._query_intersect(self.root, start, end, [])

    def _query_intersect(self, node, start, end, result = []):
        if node is None:
            return result
        if start <= node.start and node.end <= end:
            result.append(node)
        mid = (node.start + node.end)/2
        if start < mid:
            self._query_intersect(node.left, start, end, result)
        if end > mid:
            self._query_intersect(node.right, start, end, result)

        return result

    def query_sum_add(self, start, end):
        """
        Can we mix the set and add methods?
        
        >>> st = SegmentTree(range(4))
        >>> st.add(1, 3, 2)
        >>> st.query_sum_add(1, 3)
        6
        >>> st.query_sum_add(2, 3)
        4
        >>> st.query_sum_add(0, 1)
        2
        >>> st.query_sum_add(0, 0)
        0
        >>> st.query_sum_add(1, 1)
        2
        >>> st.query_sum_add(2, 2)
        2
        >>> st.pprint() # doctest: +SKIP
        """
        return self._query_sum_add(self.root, start, end)

    def _query_sum_add(self, node, start, end):
        result = 0
        
        if node is None:
            return
            
        if start <= node.start and node.end <= end:
            result += node.data.get('sum', 0) + \
                      node.data.get('delta', 0) * (node.end - node.start + 1)
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
                result += self._query_sum_add(node.left, start, end)
            if end > mid:
                result += self._query_sum_add(node.right, start, end)
        
        return result

    def query_sum_set(self, start, end):
        """
        Can we mix the set and add methods?
        
        >>> st = SegmentTree(range(4))
        >>> st.set(1, 3, 2)
        >>> st.query_sum_set(1, 3)
        6
        >>> st.query_sum_set(2, 3)
        4
        >>> st.query_sum_set(0, 1)
        2
        >>> st.query_sum_set(0, 0)
        0
        >>> st.query_sum_set(1, 1)
        2
        >>> st.query_sum_set(2, 2)
        2
        >>> st.pprint() # doctest: +SKIP
        """
        return self._query_sum_set(self.root, start, end)

    def _query_sum_set(self, node, start, end):
        result = 0
        
        if node is None:
            return
            
        if start <= node.start and node.end <= end:
            #if node.is_same:
            result += node.calcsum()
        else:
            if node.is_same:
                if node.has_left():
                    node.left.data['value'] = node.data.get('value', 0)
                    node.left.is_same = True
                if node.has_right():
                    node.right.data['value'] = node.data.get('value', 0)
                    node.right.is_same = True
                node.is_same = False
            mid = (node.start + node.end)/2
            if start <= mid:
                result += self._query_sum_set(node.left, start, end)
            if end > mid:
                result += self._query_sum_set(node.right, start, end)
        
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
        >>> st.query_sum_add(1, 3)
        6
        >>> st.query_sum_add(2, 3)
        4
        >>> st.query_sum_add(0, 1)
        2
        >>> st.query_sum_add(0, 0)
        0
        >>> st.query_sum_add(1, 1)
        2
        >>> st.query_sum_add(2, 2)
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
            node.data['max'] = node.data.get('max', 0) + max(
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
        >>> st.query_sum_set(1, 3)
        6
        >>> st.query_sum_set(2, 3)
        4
        >>> st.query_sum_set(0, 1)
        2
        >>> st.query_sum_set(0, 0)
        0
        >>> st.query_sum_set(1, 1)
        2
        >>> st.query_sum_set(2, 2)
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


################################################################################

class hdu1166(SegmentTree):
    """
    Enemy lineup.
    
    TYPE
    ----
    
      - UPDATE: Single-point increase or decrease
      - QUERY : Sum query
        
    """
    
    name = 'Enemy lineup'
    url = 'http://acm.hdu.edu.cn/showproblem.php?pid=1166'
    label = 'SegmentTree, segment tree'

    def push_up(self, node):
        node.data['sum'] = node.left.data.get('sum', 0) +\
                           node.right.data.get('sum', 0)

    def build(self, points):
        n = len(points)
        if n < 1:
            return None
        m = (n+1)/2
        node = Node(points[0], points[-1])
        if n == 1:
            node.data['sum'] = points[0]
        else:
            node.left = self.build(points[:m])
            if node.left:
                node.left.parent = node
            node.right = self.build(points[m:])
            if node.right:
                node.right.parent = node
            self.push_up(node)

        return node

    def query(self, start, end, node = None):
        result = 0
        
        if node is None:
            node = self.root
        if node is None:
            return 
            
        if start <= node.start and node.end <= end:
            result = node.data.get('sum', 0)
        else:
            mid = (node.start + node.end)/2
            if start <= mid:
                result += self.query(start, end, node.left)
            if end > mid:
                result += self.query(start, end, node.right)
        
        return result
    
    def update(self, x, delta, node = None):
        if node is None:
            node = self.root
        if node is None:
            return
            
        if node.is_leaf():
            node.data['sum'] = node.data.get('sum', 0) + delta
        else:
            mid = (node.start + node.end)/2
            if x <= mid:
                self.update(x, delta, node.left)
            else:
                self.update(x, delta, node.right)
            self.push_up(node)
    
    @staticmethod
    def sample():
        """
        >>> hdu1166.sample()
        Case 1:
        6
        33
        59
        """
        input = """\
            1
            10
            1 2 3 4 5 6 7 8 9 10
            Query 1 3
            Add 3 6
            Query 2 7
            Sub 10 2
            Add 6 3
            Query 3 10
            End"""
        
        with BytesIO(input) as f:
            ncase = int(f.readline())
            for i in range(1, ncase+1):
                print 'Case %s:' % i
                ncamp = int(f.readline())
                nicamp = [int(e) for e in f.readline().split()]
                st = hdu1166(nicamp)
                line = f.readline().strip()
                while line != 'End':
                    a, b = [int(e) for e in line.split()[1:]]
                    if line.startswith('Q'):
                        print st.query(a, b)
                    elif line.startswith('A'):
                        st.update(a, b)
                    elif line.startswith('S'):
                        st.update(a, -b)
                    else:
                        pass
                    line = f.readline().strip()

    @staticmethod
    def generate_data():
        """
        >>> hdu1166.generate_data() # doctest: +SKIP
        """
        with open(join(DATA_PATH, 'hdu1166.dat'), 'w') as f:
            f.write('1\n')
            ncamp = 50
            f.write('%s\n' % ncamp)
            nicamp = ' '.join([str(e) for e in random.sample(range(1, ncamp+1), ncamp)])
            f.write('%s\n' % nicamp)
            for i in range(40000):
                cmd = random.choice(['Query', 'Add', 'Sub'])
                r501 = random.randint(1, 50)
                r502 = random.randint(r501, 50)
                r30 = random.randint(1, 30)
                if cmd == 'Query':
                    f.write('%s %s %s\n' % (cmd, r501, r502))
                else:
                    f.write('%s %s %s\n' % (cmd, r501, r30))
            f.write('End')

    @staticmethod
    def benchmark():
        """
        >>> hdu1166.benchmark() # doctest: +SKIP
        """
        with open(join(DATA_PATH, 'hdu1166.dat')) as f:
            ncase = int(f.readline())
            for i in range(1, ncase+1):
                print 'Case %s:' % i
                ncamp = int(f.readline())
                nicamp = [int(e) for e in f.readline().split()]
                st = hdu1166(nicamp)
                line = f.readline().strip()
                while line != 'End':
                    a, b = [int(e) for e in line.split()[1:]]
                    if line.startswith('Q'):
                        print st.query(a, b)
                    elif line.startswith('A'):
                        st.update(a, b)
                    elif line.startswith('S'):
                        st.update(a, -b)
                    else:
                        pass
                    line = f.readline().strip()

    @staticmethod
    def naive():
        pass

################################################################################

class hdu1754(SegmentTree):
    """
    I Hate It.
    
    TYPE
    ----
    
      - UPDATE: Single-point replacement.
      - QUERY : Max query
        
    """
    
    name = 'I Hate It'
    url = 'http://acm.hdu.edu.cn/showproblem.php?pid=1754'
    label = 'SegmentTree, segment tree'

    def push_up(self, node):
        node.data['max'] = max(node.left.data.get('max', 0),
                               node.right.data.get('max', 0))

    def build(self, points):
        n = len(points)
        if n < 1:
            return None
        m = (n+1)/2
        node = Node(points[0], points[-1])
        if n == 1:
            node.data['max'] = points[0]
        else:
            node.left = self.build(points[:m])
            if node.left:
                node.left.parent = node
            node.right = self.build(points[m:])
            if node.right:
                node.right.parent = node
            self.push_up(node)

        return node

    def query(self, start, end, node = None):
        result = 0
        
        if node is None:
            node = self.root
        if node is None:
            return 
            
        if start <= node.start and node.end <= end:
            result = node.data.get('max', 0)
        else:
            mid = (node.start + node.end)/2
            if start <= mid:
                result = max(result, self.query(start, end, node.left))
            if end > mid:
                result = max(result, self.query(start, end, node.right))
        
        return result
    
    def update(self, x, value, node = None):
        if node is None:
            node = self.root
        if node is None:
            return
            
        if node.is_leaf():
            node.data['max'] = value
        else:
            mid = (node.start + node.end)/2
            if x <= mid:
                self.update(x, value, node.left)
            else:
                self.update(x, value, node.right)
            self.push_up(node)
    
    @staticmethod
    def sample():
        """
        >>> hdu1754.sample()
        5
        6
        5
        9
        """
        input = """\
            5 6
            1 2 3 4 5
            Q 1 5
            U 3 6
            Q 3 4
            Q 4 5
            U 2 9
            Q 1 5"""
        
        with BytesIO(input) as f:
            np, nq = [int(e) for e in f.readline().split()]
            nip = [int(e) for e in f.readline().split()]
            st = hdu1754(nip)
            line = f.readline().strip()
            while line:
                a, b = [int(e) for e in line.split()[1:]]
                if line.startswith('Q'):
                    print st.query(a, b)
                elif line.startswith('U'):
                    st.update(a, b)
                else:
                    pass
                line = f.readline().strip()

    @staticmethod
    def generate_data():
        pass

    @staticmethod
    def benchmark():
        pass

    @staticmethod
    def naive():
        pass

################################################################################

class poj3468(SegmentTree):
    """
    A Simple Problem with Integers.
    
    TYPE
    ----
    
      - UPDATE: Interval increase or decrease.
      - QUERY : Sum query
        
    """

    name = 'A Simple Problem with Integers'
    url = 'http://poj.org/problem?id=3468'
    labels = 'SegmentTree, segment tree'
    
    def push_up(self, node):
        node.data['sum'] = node.left.data.get('sum', 0) +\
                           node.right.data.get('sum', 0)

    def push_down(self, node):
        delta = node.data.get('delta', 0)
        if delta:
            node.left.data['delta'] = node.left.data.get('delta', 0) + delta
            node.right.data['delta'] = node.right.data.get('delta', 0) + delta
            node.left.data['sum'] = node.left.data.get('sum', 0) + \
                                    delta * (node.left.end-node.left.start+1)
            node.right.data['sum'] = node.right.data.get('sum', 0) + \
                                    delta * (node.right.end-node.right.start+1)
            node.data['delta'] = 0

    def build(self, points):
        n = len(points)
        if n < 1:
            return None
        m = (n+1)/2
        node = Node(points[0], points[-1])
        if n == 1:
            node.data['sum'] = points[0]
        else:
            node.left = self.build(points[:m])
            if node.left:
                node.left.parent = node
            node.right = self.build(points[m:])
            if node.right:
                node.right.parent = node
            self.push_up(node)

        return node

    def query(self, start, end, node = None):
        result = 0
        
        if node is None:
            node = self.root
        if node is None:
            return 
            
        if start <= node.start and node.end <= end:
            result = node.data.get('sum', 0)
        else:
            self.push_down(node)
            mid = (node.start + node.end)/2
            if start <= mid:
                result += self.query(start, end, node.left)
            if end > mid:
                result += self.query(start, end, node.right)
        
        return result
    
    def update(self, start, end, delta, node = None):
        if node is None:
            node = self.root
        if node is None:
            return
            
        if start <= node.start and node.end <= end:
            node.data['delta'] = node.data.get('delta', 0) + delta
            node.data['sum'] = node.data.get('sum', 0) + \
                               delta * (node.end - node.start + 1)
        else:
            self.push_down(node)
            mid = (node.start + node.end)/2
            if start <= mid:
                self.update(start, end, delta, node.left)
            if mid < end:
                self.update(start, end, delta, node.right)
            self.push_up(node)

    @staticmethod
    def sample():
        """
        >>> poj3468.sample()
        4
        55
        9
        15
        """
        input = """\
            10 5
            1 2 3 4 5 6 7 8 9 10
            Q 4 4
            Q 1 10
            Q 2 4
            C 3 6 3
            Q 2 4"""
        
        with BytesIO(input) as f:
            np, nq = [int(e) for e in f.readline().split()]
            nip = [int(e) for e in f.readline().split()]
            st = poj3468(nip)
            line = f.readline().strip()
            while line:
                param = tuple(int(e) for e in line.split()[1:])
                if line.startswith('Q'):
                    print st.query(*param)
                elif line.startswith('C'):
                    st.update(*param)
                else:
                    pass
                line = f.readline().strip()

    @staticmethod
    def generate_data():
        pass

    @staticmethod
    def benchmark():
        pass

    @staticmethod
    def naive():
        pass

################################################################################

class poj2528(SegmentTree):
    """
    Mayor's posters.
    
    TYPE
    ----
    
      - UPDATE: Interval replacement.
      - QUERY : Hash query

    """
    
    name = "Mayor's posters"
    url = 'http://poj.org/problem?id=2528'
    labels = 'SegmentTree, segment tree'

    def push_down(self, node):
        value = node.data.get('value', 0)
        if value:
            if node.has_left():
                node.left.data['value'] = value
            if node.has_right():
                node.right.data['value'] = value
            node.data['value'] = 0

    def build(self, points):
        n = len(points)
        if n < 1:
            return None
        m = (n+1)/2
        node = Node(points[0], points[-1])
        if n == 1:
            node.data['value'] = 0
        else:
            node.left = self.build(points[:m])
            if node.left:
                node.left.parent = node
            node.right = self.build(points[m:])
            if node.right:
                node.right.parent = node

        return node

    def query(self, result = set(), node = None):
        if node is None:
            node = self.root
        if node is None:
            return 

        if node.is_leaf():
            nv = node.data.get('value')
            if nv > 0:
                result.add(nv)
        else:
            self.push_down(node)
            self.query(result, node.left)
            self.query(result, node.right)
           
        return len(result)
    
    def update(self, start, end, value, node = None):
        if node is None:
            node = self.root
        if node is None:
            return
        
        #self.push_down(node)
        if start <= node.start and node.end <= end:
            node.data['value'] = value
        else:
            self.push_down(node)
            mid = (node.start + node.end)/2
            # start <= mid leads to dead loop, how to do? insert middle in interval which range > 1
            if start <= mid:
                self.update(start, end, value, node.left)
            if end > mid:
                self.update(start, end, value, node.right)

    @staticmethod
    def sample():
        """
        Something wrong on node[2,2], it should be with 2 as value!
                                           1,10:0
                           /                                   \
                       1,4:0                                    6,10:0
                 /              \                         /               \
             1,2:0               3,4:0                6,7:0                8,10:0
            /    \              /    \               /    \               /     \
        1,1:1     2,2:1     3,3:4     4,4:4      6,6:2     7,7:5      8,8:5      10,10:5
        >>> poj2528.sample()
        4
        """
        input = """\
            1
            5
            1 4
            2 6
            8 10
            3 4
            7 10"""
        
        with BytesIO(input) as f:
            ncase = int(f.readline())
            for i in range(1, ncase+1):
                np = int(f.readline())
                pos = f.tell()
                line = f.readline().strip()
                points = set()
                while line:
                    a, b = [int(e) for e in line.split()]
                    points.add(a)
                    points.add(b)
                    line = f.readline().strip()
                points = list(points)
                for i in range(1, len(points))[::-1]:
                    if points[i] > points[i-1] + 1:
                        points.append((points[i-1] + 1))
                st = poj2528(points)
                f.seek(pos)
                line = f.readline().strip()
                value = 0
                while line:
                    value += 1
                    a, b = [int(e) for e in line.split()]
                    st.update(a, b, value)
                    line = f.readline().strip()
                print st.query()
                #st.pprint()

    @staticmethod
    def generate_data():
        pass

    @staticmethod
    def benchmark():
        pass

    @staticmethod
    def naive():
        pass

################################################################################

class poj3225(SegmentTree):
    """
    Help with Intervals.
    
    TYPE
    ----
    
      - UPDATE: Interval replacement, interval XOR.
      - QUERY : Hash query

    """

    name = 'Help with Intervals'
    url = 'http://poj.org/problem?id=3225'
    labels = 'SegmentTree, segment tree'


################################################################################

class poj3667(SegmentTree):
    """
    Hotel.
    
    TYPE
    ----
    
      - UPDATE: Interval replacement, interval XOR.
      - QUERY : Breakpoints leftmost query

    """

    name = 'Hotel'
    url = 'http://poj.org/problem?id=3667'
    labels = 'SegmentTree, segment tree'

################################################################################


class hdu1542(SegmentTree):
    """
    Atlantis.
    
    TYPE
    ----
    
    Scan line problem.
    
      - UPDATE: Interval increase and decrease.
      - QUERY : Root node query

    """

    name = 'Atlantis'
    url = 'http://acm.hdu.edu.cn/showproblem.php?pid=1542'
    labels = 'SegmentTree, segment tree'

################################################################################


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #poj3468.sample()
    #poj2528.sample()
