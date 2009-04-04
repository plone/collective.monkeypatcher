# -*- coding: utf-8
# $Id$
"""Class, function and patch for test cases"""

class Dummy(object):

    def someMethod(self):
        """someMethod docstring"""
        return "original"

def patchedMethod(self):
    """patchedMethod docstring"""
    return "patched"


def someFunction(value):
    """someFunction docstring"""
    return value

def patchedFunction(value):
    """patchedFunction docstring"""
    return value * 2

