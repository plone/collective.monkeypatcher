"""Test cases"""

from . import common
from . import dummypatch
from collective.monkeypatcher.interfaces import IMonkeyPatchEvent


class TestMonkeyPatcher(common.MonkeypatcherTestCase):
    """We test all in this class"""

    def test_patchedClass(self):
        """We have our Dummy class's someMethod patched"""

        # Testing applyed patch
        ob = dummypatch.Dummy()
        self.assertEqual(ob.someMethod(), "patched")

        # Testing docstring preservation
        docstring = dummypatch.Dummy.someMethod.__doc__
        self.assertEqual(docstring, "someMethod docstring")
        return

    def test_patchedFunction(self):
        """We have our someFunction patched"""

        # Testing applyed patch
        self.assertEqual(dummypatch.someFunction(1), 2)

        # Testing docstring monkeypatch note
        docstring = dummypatch.someFunction.__doc__
        self.assertTrue(docstring.startswith("someFunction docstring"))
        self.assertTrue(docstring.endswith(
            "'collective.monkeypatcher.tests.dummypatch.patchedFunction'"))
        return

    def test_patchWithHandler(self):
        """Patch applied with personal handler"""

        ob = dummypatch.Foo()
        self.assertEqual(ob.someFooMethod(), "patchedFooMethod result")
        return

    def test_patchWithBuiltin(self):
        """see https://github.com/plone/collective.monkeypatcher/pull/2
        """
        ob = dummypatch.Foo()
        self.assertEqual(ob.config, (1, 2))
        return

    def test_monkeyPatchEvent(self):
        """Do we notify ?"""

        events = dummypatch.all_patches
        expected_keys = {
            'description', 'original', 'replacement', 'zcml_info'}
        self.assertEqual(len(events), 4)
        for event in events:

            # Interface conformance
            self.assertTrue(IMonkeyPatchEvent.providedBy(event))

            # Checking available infos
            info_keys = set(event.patch_info.keys())
            self.assertEqual(info_keys, expected_keys)
        return


def test_suite():
    import unittest

    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromTestCase(TestMonkeyPatcher),
    ))
