"""
Demonstrates the implementation of a Bloom filter, see:
http://en.wikipedia.org/wiki/Bloom_filter
"""

import hashlib
from math import exp, log
import time
import string
import random

from bitarray import bitarray

from decorators import timethis

################################################################################

class BloomFilter(object):

    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.array = bitarray(m)
        self.array.setall(0)

    def add(self, key):
        for i in self._hashes(key):
            self.array[i] = 1

    def contains(self, key):
        return all(self.array[i] for i in self._hashes(key))

    def _hashes(self, key):
        """
        generate k different hashes, each of which maps a key to one of
        the m array positions with a uniform random distribution
        """
        h = hashlib.new('md5')
        h.update(str(key))
        x = long(h.hexdigest(), 16)
        for _ in xrange(self.k):
            if x < self.m:
                h.update('.')
                x = long(h.hexdigest(), 16)
            x, y = divmod(x, self.m)
            yield y

################################################################################

@timethis
def test_bloom(m, k, n):
    b = BloomFilter(m, k)
    for i in xrange(n):
        b.add(i)
        assert b.contains(i)

    p = (1.0 - exp(-k * (n + 0.5) / (m - 1))) ** k
    print 100.0 * p, '%'

    N = 100000
    false_pos = sum(b.contains(i) for i in xrange(n, n + N))
    print 100.0 * false_pos / N, '%'

################################################################################

def generate(filename = 'urlA.dat', n = 1000000):
    with open(filename, 'w') as f:
        letters = string.letters[:26]
        for i in xrange(n):
            d1 = random.choice(['com', 'cn', 'net', 'org'])
            d2 = ''.join(random.sample(letters, 6))
            d3 = ''.join(random.sample(letters, 3))
            line = 'http://www.%s.%s\n' % (d2, d1)
            f.write(line)

################################################################################

@timethis
def validate():
    """
    Profile result:
    
      time consuming: 4.18799996376
      memory consuming: 70 MB
      1463
    """
    result = set()
    A = set()
    
    with open('urlA.dat') as f:
        for line in f:
            A.add(line.strip())
    
    with open('urlB.dat') as f:
        for line in f:
            ip = line.strip()
            if ip in A:
                result.add(ip)
                
    return result

################################################################################

@timethis
def intersect(m, k):
    """
    Profile result:
    
      time consuming: 95.6870000362
      memory consuming: 18 MB
      1463
    """
    result = set()
    b = BloomFilter(m, k)
    with open('urlA.dat') as f:
        for line in f:
            b.add(line.strip())
            
    with open('urlB.dat') as f:
        for line in f:
            url = line.strip()
            if b.contains(url):
                result.add(url)
    
    return result

################################################################################

if __name__ == '__main__':
    #generate()
    #generate('urlB.dat')
    #print len(validate())
    print len(intersect(100000000, 6))
