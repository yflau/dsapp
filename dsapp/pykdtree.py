#! /usr/bin/env python
# coding: utf-8

def variance(a):
    """
    >>> a = [2, 5, 9, 4, 8, 7]
    >>> variance(a)
    5.805555555555556
    >>> b = [3, 4, 6, 7, 1, 1]
    >>> variance(b)
    5.222222222222222
    """
    n = len(a)
    mean = float(sum(a))/n
    variance = float(sum([pow((e-mean), 2) for e in a]))/n
    
    return variance

if __name__ == '__main__':
    import doctest
    doctest.testmod()
