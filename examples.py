#! /usr/bin/env python
#coding: utf-8

import time
import random
import string
from datetime import datetime

from tree import BinarySearchTree
from decorators import profile, profileit, print_stats

@profileit
def generate_data(number = 300000):
    """Format: 2013-07-14 20:31:45 liuyun"""
    startdate = int(time.mktime(datetime(2013, 5, 1).timetuple()))
    enddate = int(time.mktime(datetime(2013, 8, 31).timetuple()))
    with open('test.dat', 'w') as f:
        for i in xrange(number):
            timestamp = random.randint(startdate, enddate)
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)))
            f.write('    ')
            f.write(''.join(random.sample(string.letters, 6)))
            f.write('\n')


def compare():
    d = {}
    t = BinarySearchTree()
    with open('test.dat', 'r') as f:
        for line in f:
            time, user = line.rsplit(' ', 1)
            d[time] = user
            t.put(time, user)
    tmin = '2013-07-01 12:00:00'
    tmax = '2013-07-10 12:00:00'
    t0 = time.time()
    print [e if tmin < e < tmax for e in d]
    t1 = time.time()
    print 'Time-consuming(dict) is: %s' %(t1 - t0)
    
            


if __name__ == '__main__':
    generate_data()

