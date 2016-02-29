"""
Nice sorting functions

This module only provides comparators

Usage:

    list.sort(smartAlphaCompare)
    
"""
import re


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
    
    return cmp(sa_format(a), sa_format(b))

