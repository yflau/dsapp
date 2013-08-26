#! /usr/bin/env python
# coding: utf-8

"""
String match algorithms.

- standard lib: string, re
- common algorithms: naive, robin-karp, BM, KMP, Aho-Corasick, ...
- 3rd party lib: ahocorasick, re2, esmre, acora, ...

reference:

- http://www-igm.univ-mlv.fr/~lecroq/string/

"""

import string
import random

DIGITS = string.digits
LETTERS = string.ascii_lowercase

################################################################################

# Based on chapter 32 of Introduction to Algorithms(Second Edition).

def naive_string_matcher(T, P):
    """O((n-m+1)m)"""
    result = []
    n = len(T)
    m = len(P)
    for i in xrange(n-m+1):
        if P == T[i:i+m]:
            result.append(i)
            print i
    
    return result

def rkhash(P, s, q):
    m = len(P)
    d = len(s)
    p = 0
    for i in range(m):
        p = (d * p + s.index(P[i])) % q
    
    return p

def rabin_karp_matcher(T, P, sigma, q):
    """s : Character Set."""
    result = []
    n = len(T)
    m = len(P)
    d = len(sigma)
    h = pow(d, m-1) % q
    p = 0
    t = 0
    for i in range(m):
        p = (d * p + sigma.index(P[i])) % q
        t = (d * t + sigma.index(T[i])) % q
    for i in xrange(n-m+1):
        if p == t:
            if P == T[i:i+m]:
                result.append(i)
                print 'Match @', i
            else:
                print 'Pseudo-Hit @', i
        if i < n-m:
            t = (d * (t - sigma.index(T[i]) * h) + sigma.index(T[i+m])) % q
    
    return result

def rabin_karp_multiple(T, PS, sigma, q):
    """Multiple pattern match."""
    result = {}
    n = len(T)
    m = min([len(P) for P in PS])
    ps = {}
    d = len(sigma)
    h = pow(d, m-1) % q
    t = 0
    for P in PS:
        p = 0
        for i in range(m):
            p = (d * p + sigma.index(P[i])) % q
        ps[p] = P
    for i in range(m):
        t = (d * t + sigma.index(T[i])) % q
    for i in xrange(n-m+1):
        if t in ps:
            P = ps[t]
            if T[i:i+len(P)] == P:
                result.setdefault(P, []).append(i)
                print 'Match @', i
            else:
                print 'Pseudo-Hit @', i
        if i < n-m:
            t = (d * (t - sigma.index(T[i]) * h) + sigma.index(T[i+m])) % q
    
    return result

def finite_automation_matcher(T, delta, m):
    result = []
    n = len(T)
    q = 0
    
    for i in xrange(1, n+1):
        q = delta.get((q, T[i-1]))
        if q == m:
            print q
            result.append(i-m)
            print 'Match @', i-m
    
    return result

def compute_transition_function(P, sigma = LETTERS):
    delta = {}
    m = len(P)
    
    for q in range(m+1):
        kr = min(m, q+1)   # maximum state for current q
        for a in sigma:
            k = kr
            Pqa = '%s%s' % (P[:q], a)
            while not Pqa.endswith(P[:k]) and k > 0:
                k -= 1
            delta[(q, a)] = k
    
    return delta

def test_finite_automation_matcher(T, P, sigma = LETTERS):
    from pprint import pprint
    m = len(P)
    delta = compute_transition_function(P, sigma)
    pprint(delta)
    return finite_automation_matcher(T, delta, m)

################################################################################

def random_string(length, s = LETTERS):
    d = len(s)
    q, r = divmod(length, d)   # quotient and reminder
    rs = []
    for i in range(q):
        rs.extend(random.sample(s, d))
    rs.extend(random.sample(s, r))
    
    return ''.join(rs)

rs = random_string

def print_match(T, P, mi):
    m = len(P)
    print T
    for i in mi:
        print P.rjust(i+m)

pm = print_match

if __name__ == '__main__':
    import string
    #naive_string_matcher('abcdef', 'def')
    T = '3141592653589793'
    P = '26'
    mi = rabin_karp_matcher(T, P, DIGITS, 11)
    print_match(T, P, mi)
    T = rs(50)
    P = 'de'
    mi = rabin_karp_matcher(T, P, LETTERS, 17)
    pm(T, P, mi)
    
    PL = ['abc', 'aaabc', 'aabc']
    for P in PL:
        print P, rkhash(P, LETTERS, 19)
    print 'kjkj', rkhash('kjkj', LETTERS, 121)
    print 'kjk', rkhash('kjk', LETTERS, 121)
    
    T = 'abcdefhijkjkjisijiejm'
    PS = ['def', 'jie', 'kj']
    r = rabin_karp_multiple(T, PS, LETTERS, 121)
    for e in r.items():
        pm(T, *e)
    
    T = 'aaababaabaababaab'
    P = 'aabab'
    mi = test_finite_automation_matcher(T, P, 'ab')
    print mi
    pm(T, P, mi)

