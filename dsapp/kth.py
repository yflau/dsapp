#! /usr/bin/env python
# coding: utf-8

import random

def select(a, k):
    pass

def rselect(a, k):
    """random select.
    >>> a = range(1, 99)
    >>> rselect(a, 68)
    68
    """
    print len(a)
    v = random.choice(a)
    
    A1 = []
    A2 = [v]
    A3 = []
    
    for e in a:
        if e < v:
            A1.append(e)
        elif e > v:
            A3.append(e)
        else:
            pass
    
    n1 = len(A1)
    if n1 >= k:
        return rselect(A1, k)
    elif n1 + 1 >= k:
        return v
    else:
        return rselect(A3, k-n1-1)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
