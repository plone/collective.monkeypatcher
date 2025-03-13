"""ZCML handling, and applying patch"""

from . import interfaces
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as distribution_version
from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import PythonIdentifier
from zope.event import notify
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import Int
from zope.schema import Text

import logging
import re


log = logging.getLogger("collective.monkeypatcher")


class IMonkeyPatchDirective(Interface):
    """ZCML directive to apply a monkey patch late in the configuration cycle.

    This version replaces one object with another.
    """

    class_ = GlobalObject(title="The class being patched", required=False)
    module = GlobalObject(title="The module being patched", required=False)
    handler = GlobalObject(
        title="A function to perform the patching.",
        description=(
            "Must take three parameters: class/module, original (string),"
            " and replacement"
        ),
        required=False,
    )
    original = PythonIdentifier(title="Method or function to replace")
    replacement = GlobalObject(title="Method to function to replace with")
    preservedoc = Bool(title="Preserve docstrings?", required=False, default=True)
    preserveOriginal = Bool(
        title=(
            "Preserve the original function so that it is reachable view"
            " prefix _old_. Only works for def handler."
        ),
        default=False,
        required=False,
    )
    preconditions = Text(
        title=(
            "Preconditions (multiple, separated by space) to be satisfied"
            " before applying this patch. Example:"
            " Products.LinguaPlone-=1.4.3. This precondition is true if"
            " the version of Products.LinguaPlone is less than or equal to 1.4.3."
            " Note: if the package of the precondition is not available, the"
            " precondition is true, which may be surprising. You can additionally use"
            ' zcml:condition="installed Products.LinguaPlone".'
        ),
        required=False,
        default="",
    )
    ignoreOriginal = Bool(
        title=(
            "Ignore if the original function isn't present on the"
            " class/module being patched"
        ),
        default=False,
    )
    docstringWarning = Bool(
        title="Add monkey patch warning in docstring", required=False, default=True
    )
    description = Text(
        title="Some comments about your monkey patch",
        required=False,
        default="(No comment)",
    )
    order = Int(title="Execution order", required=False, default=1000)


def replace(
    _context,
    original,
    replacement,
    class_=None,
    module=None,
    handler=None,
    preservedoc=True,
    docstringWarning=True,
    description="(No comment)",
    order=1000,
    ignoreOriginal=False,
    preserveOriginal=False,
    preconditions="",
):
    """ZCML directive handler"""
    if class_ is None and module is None:
        raise ConfigurationError("You must specify 'class' or 'module'")
    if class_ is not None and module is not None:
        raise ConfigurationError(
            "You must specify one of 'class' or 'module', but not both."
        )

    scope = class_ or module

    to_be_replaced = getattr(scope, original, None)

    if to_be_replaced is None and not ignoreOriginal:
        raise ConfigurationError(f"Original {original} in {str(scope)} not found")

    if preservedoc:
        try:
            replacement.__doc__ = to_be_replaced.__doc__
        except AttributeError:
            pass

    if docstringWarning:
        try:
            patch_warning = "\n**Monkey patched by** '{}.{}'".format(
                getattr(replacement, "__module__", ""), replacement.__name__
            )
            if replacement.__doc__ is None:
                replacement.__doc__ = ""
            replacement.__doc__ += patch_warning
        except AttributeError:
            pass

    # check version
    if preconditions != "":
        if not _preconditions_matching(preconditions):
            log.info(
                "Preconditions for patching scope %s not met (%s)!",
                scope,
                preconditions,
            )
            return  # fail silently

    if handler is None:
        handler = _default_patch

        if preserveOriginal is True:
            handler = _default_preserve_handler

    _context.action(
        discriminator=None,
        callable=_do_patch,
        order=order,
        args=(handler, scope, original, replacement, repr(_context.info), description),
    )
    return


def _preconditions_matching(preconditions):
    """Return `True` if preconditions are matching."""
    matcher_r = re.compile(
        r"^(.*?)([-+!=]+)(.*)$", re.DOTALL | re.IGNORECASE | re.MULTILINE
    )
    version_r = re.compile(
        r"^([0-9]+)\.([0-9]+)\.?([0-9]?).*$", re.IGNORECASE | re.MULTILINE
    )

    # split all preconds
    for precond in preconditions.split():
        _p = precond.strip()
        package, op, version = matcher_r.search(_p).groups()
        package = package.strip()

        # first try to get package - if not found fail silently
        installed_version = None
        try:
            installed_version = distribution_version(package)
        except PackageNotFoundError:
            # Depending on the Python and setuptools versions, normalizing with
            # underscores may help.  See:
            # https://github.com/pypa/setuptools/blob/84b7b2a2f6eaf992aad6b5af923fa3f48ae7b566/setuptools/_vendor/importlib_metadata/__init__.py#L835-L839C16  # noqa: E501
            package = re.sub(r"[-_.]+", "_", package).lower()
            try:
                installed_version = distribution_version(package)
            except PackageNotFoundError:
                pass

        if not installed_version:
            # The package is not found, so we cannot check the version condition.
            # We default to returning True.  This may be surprising, but the user
            # can additionally use zcml:condition="installed <package>".
            return True

        # fill versions - we assume having s/th like
        # 1.2.3a2 or 1.2a1 or 1.2.0 - look at regexp
        p_v = list(
            map(
                int,
                [x for x in version_r.search(version).groups() if x and int(x) or 0],
            )
        )
        p_i = list(
            map(
                int,
                [
                    y
                    for y in version_r.search(installed_version).groups()
                    if y and int(y) or 0
                ],
            )
        )

        if not p_v or not p_i:
            log.error(
                "Could not patch because version not recognized. Wanted:"
                " %s, Installed: %s",
                p_v,
                p_i,
            )
            return False

        # compare operators - dumb if check - could be better
        # Note:
        # - p_v is the version parsed from the precondition
        # - p_i is the installed version
        if op == "-=":
            return p_v >= p_i
        if op == "+=":
            return p_v <= p_i
        if op == "!=":
            return p_v != p_i
        if op in ["=", "=="]:
            return p_v == p_i

        raise Exception("Unknown operator %s" % op)


@implementer(interfaces.IMonkeyPatchEvent)
class MonkeyPatchEvent:
    """Event raised when a monkeypatch is applied

    see interfaces.IMonkeyPatchEvent
    """

    def __init__(self, mp_info):
        self.patch_info = mp_info
        return


def _do_patch(handler, scope, original, replacement, zcml_info, description):
    """Apply the monkey patch through preferred method"""
    try:
        org_dotted_name = f"{scope.__module__}.{scope.__name__}.{original}"
    except AttributeError:
        org_dotted_name = f"{scope.__name__}.{original}"

    try:
        new_dotted_name = "{}.{}".format(
            getattr(replacement, "__module__", ""), replacement.__name__
        )
    except AttributeError:
        # builtins don't have __module__ and __name__
        new_dotted_name = str(replacement)

    handler_info = ""
    if handler != _default_patch:
        handler_info = " using custom handler %s" % handler

    log.debug(
        "Monkey patching %s with %s%s", org_dotted_name, new_dotted_name, handler_info
    )

    info = {
        "description": description,
        "zcml_info": zcml_info,
        "original": org_dotted_name,
        "replacement": new_dotted_name,
    }

    notify(MonkeyPatchEvent(info))
    handler(scope, original, replacement)
    return


def _default_patch(scope, original, replacement):
    """Default patch method"""
    setattr(scope, original, replacement)
    return


def _default_preserve_handler(scope, original, replacement):
    """Default handler that preserves original method"""
    OLD_NAME = "_old_%s" % original

    if not hasattr(scope, OLD_NAME):
        setattr(scope, OLD_NAME, getattr(scope, original))

    setattr(scope, original, replacement)
    return
