#! /usr/bin/env python
# coding: utf-8

################################# QUICKSORT ####################################

def partition(A, p, r):
    x = A[r]
    i = p - 1
    for j in xrange(p, r):
        if A[j] <= x:
            i += 1
            tmp = A[i]
            A[i] = A[j]
            A[j] = tmp
    tmp = A[i+1]
    A[i+1] = A[r]
    A[r] = tmp
    
    return i+1

def quicksort(A, p, r):
    if p < r:
        q = partition(A, p, r)
        quicksort(A, p, q-1)
        quicksort(A, q+1, r)

################################ INSERTIONSORT #################################

def insertionsort(A):
    for j in xrange(1, len(A)):
        key = A[j]
        i = j - 1
        while i >= 0 and A[i] > key:
            tmp = A[i+1]
            A[i+1] = A[i]
            i -= 1
        A[i+1] = key

############################### SELECTIONSORT ##################################

def selectionsort(A):
    for i in xrange(0, len(A)-1):
        for j in xrange(i+1, len(A)):
            if A[j] < A[i]:
                tmp = A[j]
                A[j] = A[i]
                A[i] = tmp

################################# MERGESORT ####################################

def merge(A, p, q, r):
    alist = []
    i = p
    j = q
    while 1:
        if A[i] < A[j]:
            alist.append(A[i])
            i += 1
        else:
            alist.append(A[j])
            j +=1
        if i >= q:
            alist.extend(A[j:r])
            break
        if j >= r:
            alist.extend(A[i:q])
            break
            
    for i in xrange(len(alist)):
        A[p+i] = alist[i]
    
    return alist

def mergesort(A, p, r):
    if p < r-1:
        q = int((p+r)/2.)
        mergesort(A, p, q)
        mergesort(A, q, r)
        merge(A, p, q, r)


################################################################################

if __name__ == '__main__':
    import random
    n = 9
    A = range(n)
    random.shuffle(A)
    print A
    #quicksort(A, 0, len(A)-1)
    #insertionsort(A)
    #selectionsort(A)
    #print merge(A, 0, 4, n)
    mergesort(A, 0, n)
    print A
