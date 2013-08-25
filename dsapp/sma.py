#! /usr/bin/env python
# coding: utf-8

"""String match algorithms."""

import string
import random

DIGITS = string.digits
LETTERS = string.ascii_lowercase

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

def rabin_karp_matcher(T, P, s, q):
    """s : Character Set."""
    result = []
    n = len(T)
    m = len(P)
    d = len(s)
    h = pow(d, m-1) % q
    p = 0
    t = 0
    for i in range(m):
        p = (d * p + s.index(P[i])) % q
        t = (d * t + s.index(T[i])) % q
    for i in xrange(n-m+1):
        if p == t:
            if P == T[i:i+m]:
                result.append(i)
                print 'Match @', i
            else:
                print 'Pseudo-Hit @', i
        if i < n-m:
            t = (d * (t - s.index(T[i]) * h) + s.index(T[i+m])) % q
    
    return result

def rabin_karp_multiple(T, PS, s, q):
    """Multiple pattern match."""
    result = {}
    n = len(T)
    m = min([len(P) for P in PS])
    ps = {}
    d = len(s)
    h = pow(d, m-1) % q
    t = 0
    for P in PS:
        p = 0
        for i in range(m):
            p = (d * p + s.index(P[i])) % q
        ps[p] = P
    for i in range(m):
        t = (d * t + s.index(T[i])) % q
    for i in xrange(n-m+1):
        if t in ps:
            P = ps[t]
            if T[i:i+len(P)] == P:
                result.setdefault(P, []).append(i)
                print 'Match @', i
            else:
                print 'Pseudo-Hit @', i
        if i < n-m:
            t = (d * (t - s.index(T[i]) * h) + s.index(T[i+m])) % q
    
    return result

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

