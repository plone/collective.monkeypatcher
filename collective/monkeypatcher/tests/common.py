# -*- coding: utf-8
# $Id$
"""Common resources for unit testing"""

from Testing import ZopeTestCase
import Products.Five
from Products.Five import zcml
from Products.Five import fiveconfigure
import collective.monkeypatcher
import collective.monkeypatcher.tests

class MonkeypatcherTestCase(ZopeTestCase.ZopeTestCase):
    """Base for test cases"""

    def afterSetUp(self):
        fiveconfigure.debug_mode = True
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('configure.zcml', collective.monkeypatcher)
        zcml.load_config('dummypatch.zcml', collective.monkeypatcher.tests)
        fiveconfigure.debug_mode = False
        return



