"""Common resources for unit testing"""

from zope.component.testing import PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig

import collective.monkeypatcher
import unittest
import zope.component


class MonkeypatcherTestCase(PlacelessSetup, unittest.TestCase):
    """Base for test cases"""

    def setUp(self):
        XMLConfig('meta.zcml', zope.component)()
        XMLConfig('meta.zcml', collective.monkeypatcher)()
        XMLConfig('configure.zcml', collective.monkeypatcher)()
        XMLConfig('dummypatch.zcml', collective.monkeypatcher.tests)()
        return
