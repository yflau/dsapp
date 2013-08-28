#! /usr/bin/env python
# coding: utf-8

import array

def reverse(a, b, e):
    """
    >>> a = array.array('c', 'abcde')
    >>> reverse(a, 1, 4)
    array('c', 'adcbe')
    """
    h = b+(e-b)/2
    
    for k in range(b, h):
        offset = k - b
        tmp = a[k]
        a[k] = a[e-offset-1]
        a[e-offset-1] = tmp
    
    return a

def rotate(a, i):
    """
    >>> a = array.array('c', 'abcdefgh')
    >>> rotate(a, 3)
    array('c', 'defghabc')
    """
    n = len(a)
    
    reverse(a, 0, i)
    reverse(a, i, n)
    reverse(a, 0, n)
    
    return a

if __name__ == '__main__':
    import doctest
    doctest.testmod()





