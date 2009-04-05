# -*- coding: utf-8
# $Id$
import common
import dummypatch
from collective.monkeypatcher.controlpanel import ControlPanel

class TestMonkeyPatcher(common.MonkeypatcherTestCase):
    """We test all in this class"""

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

        # Testing docstring monkeypatch note
        docstring = dummypatch.someFunction.__doc__
        self.failUnless(docstring.startswith("someFunction docstring"))
        self.failUnless(docstring.endswith("'collective.monkeypatcher.tests.dummypatch.patchedFunction'"))
        return

    def test_patchWithHandler(self):
        """Patch applied with personal handler"""

        ob = dummypatch.Foo()
        self.failUnlessEqual(ob.someFooMethod(), "patchedFooMethod result")
        return

    def test_registeredPatches(self):
        """We check our control panel"""
        # The control panel is installed
        # FIXME: the Five registration of collective.monkeypatcher is too late
        # As a consequence, our placeless control panel is not available at test time.

        # self.failUnless('collective_monkeypatcher' in self.app.Control_Panel.objectIds())

        cp = ControlPanel()
        patches = cp.allPatches()

        # There may be other patches in other components so we need to filter
        patches = [p for p in patches if p['original'].startswith('collective.monkeypatcher')]
        self.failUnlessEqual(len(patches), 3)

        # Examine some of our patches
        patch = [p for p in patches if p['original'] == 'collective.monkeypatcher.tests.dummypatch.someFunction'][0]
        self.failUnlessEqual(patch['replacement'], 'collective.monkeypatcher.tests.dummypatch.patchedFunction')
        self.failUnless('dummypatch.zcml' in patch['zcml_info'])
        self.failUnlessEqual(patch['description'], "This is the reason of this monkey patch")

        patch = [p for p in patches if p['original'] == 'collective.monkeypatcher.tests.dummypatch.Dummy.someMethod'][0]
        self.failUnlessEqual(patch['replacement'], 'collective.monkeypatcher.tests.dummypatch.patchedMethod')
        self.failUnless('dummypatch.zcml' in patch['zcml_info'])
        self.failUnlessEqual(patch['description'], "(No comment)")
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMonkeyPatcher))
    return suite
