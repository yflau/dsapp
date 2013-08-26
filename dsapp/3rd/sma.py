#encoding:utf-8
#!/usr/bin/python

import time
import ahocorasick
import codecs
import esm
from acora import AcoraBuilder

dictFile = "dict.txt"
testFile = "content.txt"

class Ahocorasick(object):
    def __init__(self,dic):
        self.__tree = ahocorasick.KeywordTree()
        fp = open(dic)
        for line in fp:
            self.__tree.add(line.rstrip("\n"))
        fp.close()
        self.__tree.make()

    def findall(self,content):
        hitList = []
        for start, end in self.__tree.findall(content):
            hitList.append(content[start:end])
        return hitList

class Acora(object):

    def __init__(self,dic):
        self.__builder = AcoraBuilder()
        fp = open(dic)
        for line in fp:
            self.__builder.add(line.rstrip("\n").decode("utf-8"))
        fp.close()
        self.__tree = self.__builder.build()

    def findall(self,content):
        hitList = []
        for hitWord, pos in self.__tree.finditer(content):
            hitList.append(hitWord)
        return hitList

class Esmre(object):

    def __init__(self,dic):
        self.__index = esm.Index()
        fp = open(dic)
        for line in fp:
            self.__index.enter(line.rstrip("\n"))
        fp.close()
        self.__index.fix()

    def findall(self,content):
        hitList = []
        for pos, hitWord in self.__index.query(content):
            hitList.append(hitWord)
        return hitList

if __name__ == "__main__":
    fp = open(testFile)
    content = fp.read()
    fp.close()

    t0 = time.time()
    ahocorasick_obj = Ahocorasick(dictFile)
    t1 = time.time()
    acora_obj = Acora(dictFile)
    t2 = time.time()
    esmre_obj = Esmre(dictFile)
    t3 = time.time()

    ahocorasick_obj.findall(content)
    t4 = time.time()
    acora_obj.findall(content.decode("utf-8"))
    t5 = time.time()
    esmre_obj.findall(content)
    t6 = time.time()

    Ahocorasick_init = t1 - t0
    Acora_init = t2 - t1
    Esmre_init = t3 - t2
    Ahocorasick_process = t4 - t3
    Acora_process = t5 - t4
    Esmre_process = t6 - t5
    print "Ahocorasick init: %f" % Ahocorasick_init
    print "Acora init: %f" % Acora_init
    print "Esm_init: %f" % Esmre_init
    print "Ahocorasick process: %s" % Ahocorasick_process
    print "Acora process: %s" % Acora_process
    print "Esm_process: %f" % Esmre_process