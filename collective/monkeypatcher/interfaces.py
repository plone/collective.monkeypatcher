# -*- coding: utf-8 -*-
# $Id$
"""Public interfaces"""

from zope.interface import Interface

class IMonkeyPatchEvent(Interface):
    """Monkey patch applied event"""

    def patchInfo():
        """A dict about the patch with following keys:
        * 'description': A text that describes the monkey patch
        * 'zcml_info': A text about the ZCML portion that made the patch
        * 'original': Dotted name of the original method/function.
        * 'replacement': Dotted name of the new function
        """
        pass



