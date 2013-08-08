#!/usr/bin/env python
# -*- coding:utf-8 -*-

# * trie, prefix tree
# * Algorithm refered : http://blog.csdn.net/v_july_v/article/details/6897097
# * Codes Refered : http://blog.csdn.net/psrincsdn/article/details/8158182

class Node(object):
    def __init__(self):
        self.id = 0
        self.word = None
        self.count = 0
        self.children = {}

    def __str__(self):
        return '%s(%s, %s)' % (self.id, self.word, self.count)

class Trie(object):
    # auto inc id
    id = 0
    
    def __init__(self):
        self.root = Node()

    def insert(self, word, id = None):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.word = word
        node.count += 1

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return False, None
            node = node.children[c]
        return True, node.word

    def delete(self, word, node=None, i=0):
        node = node if node else self.root
        c = word[i]
        if c in node.children:
            child_node = node.children[c]
            if len(word)==(i+1):
                return node.children.pop(c) if len(child_node.children)==0 else False
            elif self.delete(word, child_node, i+1):
                return node.children.pop(c) if (len(child_node.children)==0 and not child_node.word) else False
        return False

    def __collect_words(self, node):
        results = []
        if node.word:
            results.append(node.word)
        for k,v in node.children.iteritems():
            results.extend(self.__collect_words(v))
        return results

    def auto_complete(self, prefix_word):
        node = self.root
        for c in prefix_word:
            if c not in node.children:
                return []
            node = node.children[c]

        return self.__collect_words(node)

    def max_word_length(self):
        return self.height()

    def __node_height(self, node_list):
        if len(node_list) == 0:
            return 0
        else:
            children_node_list = []
            [children_node_list.extend( [v for v in node.children.itervalues()] ) for node in node_list]
            return 1 + self.__node_height(children_node_list)

    def height(self):
        return 0 if not self.root.children else self.__node_height([v for v in self.root.children.itervalues()])

    # basic methods
    def preorder(self):
        return self._preorder(self.root)
    
    def _preorder(self, node):
        results = []
        if node.word:
            results.append(node.word)
        for k,v in node.children.iteritems():
            results.extend(self._preorder(v))
        return results

    def ipreorder(self, node):
        if node.word:
            yield (node.count, node.word)
        for k, v in node.children.iteritems():
            for e in self.ipreorder(v):
                yield e

    def pprint(self, node):
        while node.children:
            print node
            for k, v in node.children.iteritems():
                print v
                node = v

################################################################################

from memory_profiler import profile

@profile
def test():
    t = Trie()
    with open('%s.dat' % __file__) as f:
        for line in f:
            t.insert(line.split()[-1])
    print t.search('to')
    print t.auto_complete('to')



if __name__ == '__main__':
    #test()
    t = Trie()
    t.insert('abcd')
    t.insert('ab')
    t.insert('best')
    t.insert('better')
    t.insert('best')
    for e in t.ipreorder(t.root):
        print e
    t.pprint(t.root)



