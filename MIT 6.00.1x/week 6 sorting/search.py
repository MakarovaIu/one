# -*- coding: utf-8 -*-
"""
Created on Wed May 18 20:26:49 2016

@author: ericgrimson
"""

def search1(L, e):
    def bSearch(L, e, low, high):
        if high == low:
            return L[low] == e
        mid = low + int((high - low)/2)
        if L[mid] == e:
            return True
        if L[mid] > e:
            return bSearch(L, e, low, mid - 1)
        else:
            return bSearch(L, e, mid + 1, high)

    if len(L) == 0:
        return False
    else:
        return bSearch(L, e, 0, len(L) - 1)


def search(L, e):
    for i in range(len(L)):
        if L[i] == e:
            return True
        if L[i] > e:
            return False
    return False


def newsearch(L, e):
    for i in range(len(L)):
        print(L[len(L)-i-1])
        print(L[i])
        if L[len(L)-i-1] == e:
            return True
        if L[i] < e:
            return False
    return False

l = [0,3,5]


def swapSort(L):
    """ L is a list on integers """
    print("Original L: ", L)
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            print(L[j],L[i])
            if L[j] < L[i]:
                # the next line is a short
                # form for swap L[i] and L[j]
                L[j], L[i] = L[i], L[j]
                print(L)
    print("Final L: ", L)


def modSwapSort(L):
    """ L is a list on integers """
    print("Original L: ", L)
    for i in range(len(L)):
        for j in range(len(L)):
            print(L[j],L[i])
            if L[j] < L[i]:
                # the next line is a short
                # form for swap L[i] and L[j]
                L[j], L[i] = L[i], L[j]
                print(L)
    print("Final L: ", L)