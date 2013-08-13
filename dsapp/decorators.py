#! /usr/bin/env python
# coding: utf-8

################################################################################
# took codes from the following:
#
# - [Python Wiki - Smart deprecation warnings ](http://wiki.python.org/moin/PythonDecoratorLibrary#Smart_deprecation_warnings_.28with_valid_filenames.2C_line_numbers.2C_etc..29)
# - [Active Code Stack - deprecated ](http://code.activestate.com/recipes/391367-deprecated/)
# - http://hychen.wuweig.org/blog/2011/12/18/recipe-deprecated-function-in-python/
#
#
#import os
#import warnings
#import functools
#
## enable to show warring
#warnings.simplefilter('default')
#
#def deprecated(replacement=None):
#    """This is a decorator which can be used to mark functions
#    as deprecated. It will result in a warning being emitted
#    when the function is used.
#
#    ref:
#        - recipe-391367-1 on active stack code
#        - recipe-577819-1 on active stack code
#
#    @replacement function replacement function
#    """
#    def wrapper(old_func):
#        wrapped_func = replacement and replacement or old_func
#        @functools.wraps(wrapped_func)
#        def new_func(*args, **kwargs):
#            msg = "Call to deprecated function %(funcname)s." % {
#                    'funcname': old_func.__name__}
#            if replacement:
#                msg += "; use {} instead".format(replacement.__name__)
#            warnings.warn_explicit(msg,
#                category=DeprecationWarning,
#                filename=old_func.func_code.co_filename,
#                lineno=old_func.func_code.co_firstlineno + 1
#            )
#            return wrapped_func(*args, **kwargs)
#        return new_func
#    return wrapper
#
#def new1():
#    print 'called new1'
#
#@deprecated()
#def old1():
#    print 'called old1'
#
#@deprecated(new1)
#def old2():
#    print 'called old1'
#
#if __name__ == '__main__':
#    print old1
#    old1()
#    print old2
#    old2()
#    SomeClass().some_old_method(3, 4)
################################################################################

"""
Usage:

>>> import pstats
>>> p = pstats.Stats("xxx.profile")
>>> p.sort_stats("time").print_stats()

"""

################################ Deprecated ####################################

import warnings
import functools

warnings.simplefilter('always', DeprecationWarning)

def deprecated(func, msg=None):
    """
    A decorator which can be used to mark functions
    as deprecated.It will result in a deprecation warning being shown
    when the function is used.
    """

    message = msg or "Use of deprecated function '{}`.".format(func.__name__)

    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        warnings.warn(message, DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return wrapper_func


@deprecated
def some_old_function(x,y):
    return x + y

class SomeClass:
    @deprecated
    def some_old_method(self, x,y):
        return x + y

################################################################################

import time

def timethis(func):
    def wrap(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        #logging.info(m1.size - m0.size)
        print 'time consuming: %s ' % str(t1 - t0)
        return result
    
    return wrap

try:
    from guppy import hpy
except:
    pass

def memorythis(func):
    def wrap(*args, **kwargs):
        hp = hpy()
        m0 = hp.heap()
        result = func(*args, **kwargs)
        m1 = hp.heap()
        #logging.info(m1.size - m0.size)
        print m1.size - m0.size
        return result

    return wrap


def profile(func):
    pass

################################################################################

import timeit
import logging

def profile(func):
    def wrap(*args, **kwargs):
        t = timeit.Timer()
        result = func(*args, **kwargs)
        #logging.info(t.timeit())
        print t.timeit()
        return result

    return wrap

@profile
def foo():
    pass


import cProfile

def profileit(func):
    def wrapper(*args, **kwargs):
        datafn = func.__name__ + ".profile" # Name the data file sensibly
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.dump_stats(datafn)
        return retval

    return wrapper

@profileit
def function_you_want_to_profile():
    pass


import cProfile

def profileit2(name):
    def inner(func):
        def wrapper(*args, **kwargs):
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            # Note use of name from outer scope
            prof.dump_stats(name)
            return retval
        return wrapper
    return inner

@profileit2("profile_for_func1_001")
def func1():
    pass


def print_stats(profile):
    import pstats
    p = pstats.Stats(profile)
    p.sort_stats("time").print_stats()


if __name__=="__main__":
    some_old_function(3, 4)
    SomeClass().some_old_method(3, 4)


