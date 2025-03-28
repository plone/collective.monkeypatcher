"""Class, function and patch for test cases"""


class Dummy:
    """As said"""

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


class Foo:
    """As said"""

    config = (1, 2, 3)

    def someFooMethod(self):
        return "fooMethod result"


def patchedFooMethod(self):
    return "patchedFooMethod result"


def my_appy_patch(scope, original, replacement):
    setattr(scope, original, replacement)
    return


patchedAttribute = (1, 2)


all_patches = []


def monkeyPatchHandler(event):
    """Fake handler"""

    global all_patches
    all_patches.append(event)
    return
