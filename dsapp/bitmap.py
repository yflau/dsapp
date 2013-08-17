#! /usr/bin/env python
# coding: utf-8

"""
0.1 billion integers sort test on bitsort_xxx:

Speed(s): 
array   list   bitarray   bitstring
4.75    6.86   14.77      59.72

Memory(MB):
array   list   bitarray   bitstring
106     400    20         265
"""

import random
import time
from os.path import join, exists

from guppy import hpy
from pympler import tracker
#from memory_profiler import profile
from memprof import memprof

from decorators import timethis, memorythis, profile
from settings import DATA_PATH

TDATA = '%s.dat' % __file__
def get_data_file(filename = TDATA):
    return filename if exists(filename) else join(DATA_PATH, filename)
TDATA = get_data_file()
MAXN = 100000000

################################################################################

def generate(filename = TDATA, number = 1000000):
    with open(filename, 'w') as f:
        for i in xrange(number):
            line = '%s\n' % random.randint(1, MAXN)
            f.write(line)

################################################################################

from array import array

def bitsort_array(filename, maxn = MAXN):
    """ Sort a file named 'filename' which
    consists of maxn integers where each
    integer is less than maxn.
    
    Profile result:
    
      bitsort_array: 4.75
      memory consuming: 106 MB.
    """
    # Initialize bitmap
    a = array('c', maxn * '0')

    # Read from file and fill bitmap
    for line in file(filename):
        n = int(line.strip())
        # Turn bits on for numbers
        if n<maxn: 
            a[n] = '1'

    # Return a generator that iterates over the list
    #for n in xrange(len(a)):
    #    if a[n] == '1': 
    #        yield n

#@profile
def test_bitsort_array():
    t0 = time.time()
    bitsort_array(TDATA, MAXN)
    t1 = time.time()
    print 'bitsort_array: %s' % (t1 - t0)

################################################################################

# Python implementation of bitsort
#  algorithm from "Programming Pearls"

def bitsort_list(filename, maxn = MAXN):
    """ Sort a file named 'filename' which
    consists of maxn integers where each
    integer is less than maxn.
    
    bitsort_list: 2.15700006485
    Filename: bitmap.py
    
    Line #    Mem usage    Increment   Line Contents
    ================================================
        44                             @profile
        45     8.098 MB     0.000 MB   def test_bitsort_list():
        46     8.098 MB     0.000 MB       t0 = time.time()
        47     8.121 MB     0.023 MB       bitsort_list(TDATA, 1000000)
        48     8.121 MB     0.000 MB       t1 = time.time()
        49     8.137 MB     0.016 MB       print 'bitsort_list: %s' % (t1 - t0)
    
    Profile result:
    
      bitsort_list: 3.36000013351
      memory consuming: 400 MB.
    """
    # Initialize bitmap
    a = [0]*maxn

    # Read from file and fill bitmap
    for line in file(filename):
        n = int(line.strip())
        # Turn bits on for numbers
        if n<maxn: 
            a[n] = 1

    # Return a generator that iterates over the list
    #for n in xrange(len(a)):
    #    if a[n]==1: 
    #        yield n

#@profile
def test_bitsort_list():
    t0 = time.time()
    bitsort_list(TDATA, MAXN)
    t1 = time.time()
    print 'bitsort_list: %s' % (t1 - t0)

################################################################################

from blist import blist

@timethis
def bitsort_blist(filename = TDATA, maxn = MAXN):
    """ Sort a file named 'filename' which
    consists of maxn integers where each
    integer is less than maxn.

    Profile result:

      bitsort_blist: 4.84400010109
      memory consuming: 70 MB
    """
    # Initialize bitmap
    a = blist([0])*maxn

    # Read from file and fill bitmap
    for line in file(filename):
        n = int(line.strip())
        # Turn bits on for numbers
        if n<maxn: 
            a[n] = 1

    # Return a generator that iterates over the list
    #for n in xrange(len(a)):
    #    if a[n]==1: 
    #        yield n

#@profile
def test_bitsort_blist():
    t0 = time.time()
    bitsort_blist(TDATA, MAXN)
    t1 = time.time()
    print 'bitsort_blist: %s' % (t1 - t0)

################################################################################

import bintrees

def bitsort_avl(filename, maxn = MAXN):
    """ Sort a file named 'filename' which
    consists of maxn integers where each
    integer is less than maxn.

    Profile result:

      bitsort_avl: 
      memory consuming:
    """
    # Initialize bitmap
    a = bintrees.FastAVLTree()

    # Read from file and fill bitmap
    for line in file(filename):
        n = int(line.strip())
        # Turn bits on for numbers
        if n<maxn: 
            a.insert(1)
        else:
            a.insert(0)

    # Return a generator that iterates over the list
    #for n in xrange(len(a)):
    #    if a[n]==1: 
    #        yield n

#@profile
def test_bitsort_avl():
    t0 = time.time()
    bitsort_avl(TDATA, MAXN)
    t1 = time.time()
    print 'bitsort_avl: %s' % (t1 - t0)

################################################################################

from bitarray import bitarray

def bitsort_bitarray(filename, maxn = MAXN):
    """ Sort a file named 'filename' which
    consists of maxn integers where each
    integer is less than maxn.

    bitsort_bitarray: 2.48399996758
    Filename: bitmap.py
    
    Line #    Mem usage    Increment   Line Contents
    ================================================
        76                             @profile
        77     8.094 MB     0.000 MB   def test_bitsort_bitarray():
        78     8.094 MB     0.000 MB       t0 = time.time()
        79     8.141 MB     0.047 MB       bitsort_bitarray(TDATA, 1000000)
        80     8.141 MB     0.000 MB       t1 = time.time()
        81     8.156 MB     0.016 MB       print 'bitsort_bitarray: %s' % (t1 - t0)

    Profile result:
    
      0.1 billion:
      
      bitsort_bitarray: 14.7660000324
      memory consuming: 20 MB
      
      1 billion:
      
      bitsort_bitarray: 101.671999931
      profile result is wrong, actual memory consuming is about 131 MB.
    """
    # Initialize bitmap
    a = bitarray('0') * maxn

    # Read from file and fill bitmap
    with open(filename) as f:
        for line in f:
            n = int(line.strip())
            # Turn bits on for numbers
            if n < maxn:
                a[n] = 1

    # Return a generator that iterates over the list
    #for n in xrange(len(a)):
    #    if a[n]==1: 
    #        yield n

#@profile
def test_bitsort_bitarray():
    t0 = time.time()
    bitsort_bitarray(TDATA, MAXN)
    t1 = time.time()
    print 'bitsort_bitarray: %s' % (t1 - t0)

################################################################################

from bitstring import BitArray

def bitsort_bitstring(filename, maxn = MAXN):
    """ Sort a file named 'filename' which
    consists of maxn integers where each
    integer is less than maxn.
    
    Profile result:
    
      bitsort_bitstring: 59.7189998627
      memory consuming: 265 MB
    """
    # Initialize bitmap
    a = BitArray(bin = maxn * '0')

    # Read from file and fill bitmap
    with open(filename) as f:
        for line in f:
            n = int(line.strip())
            # Turn bits on for numbers
            if n < maxn: 
                a[n] = 1

    # Return a generator that iterates over the list
    #for n in xrange(len(a)):
    #    if a[n]==1: 
    #        yield n

#@profile
def test_bitsort_bitstring():
    t0 = time.time()
    bitsort_bitstring(TDATA, MAXN)
    t1 = time.time()
    print 'bitsort_bitstring: %s' % (t1 - t0)

################################################################################

def generate_phone_number(filename = 'phone.dat', n = 5000000):
    with open(filename, 'w') as f:
        for i in xrange(n):
            line = '6%s\n' % ''.join(random.sample('0123456789', 7))
            f.write(line)

def bitstats_bitarray(filename = 'phone.dat', maxn = MAXN):
    """
    Profile result:
    
      number of phones: 604632
      bitstats_bitarrray: 130.469000101
      Memory comsuming: 21 MB
    """
    result = 0
    a = bitarray('0') * maxn
    # Read from file and fill bitmap
    with open(filename) as f:
        for line in f:
            n = int(line.strip())
            # Turn bits on for numbers
            if n < maxn:
                a[n] = 1
                
    
    for n in xrange(len(a)):
        if a[n] == 1: 
            result += 1
    
    return result

#@profile
def test_bitstats_bitarray():
    t0 = time.time()
    #bitstats_bitarrray()
    print 'number of phones: %s' % (bitstats_bitarray())
    t1 = time.time()
    print 'bitstats_bitarrray: %s' % (t1 - t0)



def bitstats_array(filename = 'phone.dat', maxn = MAXN):
    """
    Profile result:
    
      number of phones: 604632
      time consuming: 52.8589999676
      Memory comsuming: 104 MB
    """
    result = 0
    a = array('c', maxn * '0')
    # Read from file and fill bitmap
    with open(filename) as f:
        for line in f:
            n = int(line.strip())
            # Turn bits on for numbers
            if n < maxn:
                a[n] = '1'
                
    
    for n in xrange(len(a)):
        if a[n] == '1': 
            result += 1
    
    return result

@timethis
def test_bitstats_array():
    print 'number of phones: %s' % (bitstats_array())


def validate_number_of_phones(filename = 'phone.dat'):
    """
    Profile result:
    
      number of phones: 604632
      validate_number_of_phones: 10.7190001011
      Memory consuming: 36 MB
    """
    #tr = tracker.SummaryTracker()
    #tr.print_diff() 
    #hp = hpy()
    #print hp.heap()
    s = set()
    with open(filename) as f:
        for line in f:
            s.add(line.strip())
        #tr.print_diff() 
        #print hp.heap()
    return len(s)

@timethis
def test_validate_number_of_phones():
    print 'number of phones: %s' % (validate_number_of_phones())

################################################################################

def generate_numbers(filename = 'integers.dat', n = 5000000):
    with open(filename, 'w') as f:
        for i in xrange(n):
            line = '%s\n' % random.randint(0, MAXN)
            f.write(line)

@timethis
def kbitmap(filename = 'integers.dat', maxn = MAXN, k = 2):
    """
    Profile result:
      
     5,000,000 integers:
      time consuming: 321.358999968
      memory consumiing: 50 MB
      4756694
      
     10,000,000 integers:
      time consuming: 368.875
      memory consumiing: 50 MB
      9046665
    """
    result = 0
    no = bitarray('00')
    nr = bitarray('10')
    
    a = bitarray('00') * maxn
    
    with open(filename) as f:
        for line in f:
            n = int(line.strip())
            if n < maxn:
                if a[2*n:2*n+2] == no:
                    a[2*n] = 1
                elif a[2*n:2*n+2] == nr:
                    a[2*n] = 0
                    a[2*n+1] = 1
                else:
                    pass
    
    for n in xrange(0, len(a), 2):
        if a[n:n+2] == nr:
            result += 1
    
    return result


@timethis
def kbitmap_array(filename = 'integers.dat', maxn = MAXN, k = 2):
    """
    Profile result:
    
     5,000,000 integers:
      time consuming: 82.8129999638
      memory consuming: 222 MB (max: 308 MB)
      4756694
    
     10,000,000 integers:
      time consuming: 101.905999899
      memory consuming: 222 MB (max: 416 MB)
      9046665
    """
    result = 0
    no = array('c', '00')
    nr = array('c', '10')
    
    a = array('c', '00' * maxn)
    
    with open(filename) as f:
        for line in f:
            n = int(line.strip())
            if n < maxn:
                if a[2*n:2*n+2] == no:
                    a[2*n] = '1'
                elif a[2*n:2*n+2] == nr:
                    a[2*n] = '0'
                    a[2*n+1] = '1'
                else:
                    pass
    
    for n in xrange(0, len(a), 2):
        if a[n:n+2] == nr:
            result += 1
    
    return result

@timethis
def validate_non_repeat(filename = 'integers.dat'):
    """
    Profile result:
      
     5,000,000 integers:
      time consuming: 31.7029998302
      memory consuming: 185 MB
      4756694
      
     10,000,000 integers:
      time consuming: 65.4679999352
      memory consuming: 389 MB
      9046665
    """
    d = {}
    result = 0
    with open(filename) as f:
        for line in f:
            n = int(line.strip())
            d[n] = d.setdefault(n, 0) + 1
    
    for i, n in d.iteritems():
        if n == 1:
            result += 1
    
    return result

################################################################################

if __name__=="__main__":
    #generate()
    #test_bitsort_array()
    #test_bitsort_list()
    test_bitsort_blist()
    #test_bitsort_bitarray()
    #test_bitsort_bitstring()
    
    #generate_phone_number()
    #test_bitstats_bitarray()
    #test_bitstats_array()
    #test_validate_number_of_phones()
    
    #generate_numbers('10mi.dat', 10000000)
    #print kbitmap('10mi.dat')
    #print kbitmap_array('10mi.dat')
    #print validate_non_repeat('10mi.dat')


