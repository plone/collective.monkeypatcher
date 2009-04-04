# -*- coding: utf-8
# $Id$
"""Common resources for unit testing"""

from Testing.ZopeTestCase import ZopeTestCase
from Products.Five import zcml
from Products.Five import fiveconfigure
import collective.monkeypatcher.tests

class MonkeypatcherTestCase(ZopeTestCase):
    """Base for test cases"""

    def afterSetUp(self):
        fiveconfigure.debug_mode = True
        zcml.load_config('dummypatch.zcml', collective.monkeypatcher.tests)
        fiveconfigure.debug_mode = False
        return



