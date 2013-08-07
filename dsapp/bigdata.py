#! /usr/bin/env python
# coding: utf-8

import random
import heapq
import string

################################################################################

TDATA = '%s.dat' % __file__

def generate_vast_IP(total = 10000000):
    """
    Generate only 10,000,000 ips to have a test as a demo.
    
    total: 10,000,000
    unique: 3,000,000
    time consuming:  116.20299983
    """
    with open(TDATA, 'w') as f:
        for i in xrange(total):
            b = random.randint(1, 45)
            c = random.randint(0, 256)
            d = random.randint(0, 256)
            f.write('202.%s.%s.%s\n' % (b, c, d))

def generate_words(total = 1000000):
    with open(TDATA, 'w') as f:
        letters = string.letters[:26]
        for i in xrange(total):
            ri = random.randint(2, 12)
            f.write(''.join(random.sample(letters, ri)))
            f.write('\n')

################################################################################

def find_max(tempdirs = []):
    """Method: divide-and-conquer + hash stat + sort
    
    ('202.43.158.225\n', 14)
    ('202.13.186.165\n', 14)
    ('202.13.68.3\n', 14)
    ('202.32.247.249\n', 14)
    ('202.27.42.169\n', 14)
    ('202.6.99.167\n', 15)
    ('202.39.209.255\n', 15)
    ('202.45.250.204\n', 15)
    ('202.21.31.17\n', 15)
    ('202.34.112.151\n', 15)
    """
    fd = {}
    result = []
    
    # divide+hash
    with open(TDATA) as f:
        for line in f:
            fi = '%03i' % (hash(line.strip())%100)
            if fi not in fd:
                fd[fi] = open('tmp/%s.dat'%fi, 'w+')
            fd[fi].write(line)

    # hash_stat+sort
    for fi in fd:
        f = fd[fi]
        f.flush()
        f.seek(0)
        md = {}
        for line in f:
            ip = line.strip()
            md[line] = md.setdefault(line, 0) + 1
        tmp = sorted(md.iteritems(), key=lambda d: d[1])
        result.append(tmp[-1])
        f.close()
        
    return sorted(result, key=lambda d: d[1])

################################################################################


def find_top_k(k = 10):
    """Method: divide-and-conquer + hash stat + heap
    
    time consuming:  61.2349998951
    (14, '202.40.136.38')
    (14, '202.43.158.225')
    (14, '202.44.77.103')
    (14, '202.45.235.6')
    (14, '202.9.53.21')
    (15, '202.21.31.17')
    (15, '202.34.112.151')
    (15, '202.39.209.255')
    (15, '202.45.250.204')
    (15, '202.6.99.167')
    """
    fd = {}
    result = []
    
    # divide+hash
    with open(TDATA) as f:
        for line in f:
            fi = '%03i' % (hash(line.strip())%100)
            if fi not in fd:
                fd[fi] = open('tmp/%s.dat'%fi, 'w+')
            fd[fi].write(line)

    # hash+sort
    for fi in fd:
        f = fd[fi]
        f.flush()
        f.seek(0)
        md = {}
        for line in f:
            ip = line.strip()
            md[ip] = md.setdefault(ip, 0) + 1
        for keyword, v in md.iteritems():
            if len(result) < k:
                heapq.heappush(result, (v, keyword))
            else:
                heapq.heappushpop(result, (v, keyword))
        f.close()
        
    return result

################################################################################

from trie import Trie

def find_top_k_with_trie(k = 10):
    result = []
    t = Trie()
    # trie
    with open(TDATA) as f:
        for line in f:
            t.insert(line.strip())
    
    for n in t.ipreorder(t.root):
        if len(result) < k:
            heapq.heappush(result, n)
        else:
            heapq.heappushpop(result, n)
            
    return result

################################################################################

def test(*args, **kw):
    pass

if __name__ == '__main__':
    import time
    
#    t0 = time.time()
#    generate_words(100000)
#    print 'time consuming: ', time.time() - t0

#    t0 = time.time()
#    #res = find_max()
#    res = find_top_k()
#    print 'time consuming: ', time.time() - t0
#    for i in range(10):
#        print heapq.heappop(res)

    t0 = time.time()
    res = find_top_k_with_trie()
    print 'time consuming: ', time.time() - t0
    for i in range(10):
        print heapq.heappop(res)
