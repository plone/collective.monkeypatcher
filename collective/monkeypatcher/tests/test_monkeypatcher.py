# -*- coding: utf-8
# $Id$
import common
import dummypatch

class TestMonkeyPatcher(common.MonkeypatcherTestCase):

    def test_patchedClass(self):
        """We have our Dummy class's someMethod patched"""
        # Testing applyed patch
        ob = dummypatch.Dummy()
        self.failUnlessEqual(ob.someMethod(), "patched")

        # Testing docstring preservation
        docstring = dummypatch.Dummy.someMethod.__doc__
        self.failUnlessEqual(docstring, "someMethod docstring")
        return

    def test_patchedFunction(self):
        """We have our someFunction patched"""
        # Testing applyed patch
        self.failUnlessEqual(dummypatch.someFunction(1), 2)

        # Testing docstring preservation
        docstring = dummypatch.someFunction.__doc__
        self.failUnlessEqual(docstring, "someFunction docstring")
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMonkeyPatcher))
    return suite
