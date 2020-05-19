"""
Nice sorting functions

This module only provides comparators

Usage:

    list.sort(smartAlphaCompare)
    
"""
import re


def smartAlphaFormat(str):
    convert = lambda text: int(text) if text.isdigit() else text 
    return [ convert(c) for c in re.split('([0-9]+)', str.lower()) ]


def smartAlphaCompare(a, b):
    """
    Sorts two strings by smart
        alpha numeric
        
        is case insensitive
    """
    
    # define the smart alpha format
    def sa_format(str):
        convert = lambda text: int(text) if text.isdigit() else text 
        return [ convert(c) for c in re.split('([0-9]+)', str.lower()) ]

     
    newA = sa_format(a)
    newB = sa_format(b)
    print("1")
    print(newA)
    print(newB)
    print("2")

    if (newA > newB):
        return a
    else:
        return b
    

#    return cmp(sa_format(a), sa_format(b))

