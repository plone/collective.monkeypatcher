import logging

from zope.interface import Interface

from zope.configuration.fields import GlobalObject, PythonIdentifier
from zope.configuration.exceptions import ConfigurationError

from zope.schema import Int, Bool, Text

class IMonkeyPatchDirective(Interface):
    """ZCML directive to apply a monkey patch late in the configuration cycle.

    This version replaces one object with another.
    """

    class_ = GlobalObject(title=u"The class being patched", required=False)
    module = GlobalObject(title=u"The module being patched", required=False)
    handler = GlobalObject(title=u"A function to perform the patching.",
                           description=u"Must take three parameters: class/module, original (string), and replacement",
                           required=False)
    original = PythonIdentifier(title=u"Method or function to replace")
    replacement = GlobalObject(title=u"Method to function to replace with")
    preservedoc = Bool(title=u"Preserve docstrings?", required=False, default=True)
    docstringWarning = Bool(title=u"Add monkey patch warning in docstring", required=False, default=True)
    description = Text(title=u'Some comments about your monkey patch', required=False, default=u"(No comment)")
    order = Int(title=u"Execution order", required=False, default=1000)


def replace(_context, original, replacement, class_=None, module=None, handler=None, preservedoc=True,
            docstringWarning=True, description=u"(No comment)", order=1000):
    if class_ is None and module is None:
        raise ConfigurationError(u"You must specify 'class' or 'module'")
    if class_ is not None and module is not None:
        raise ConfigurationError(u"You must specify one of 'class' or 'module', but not both.")

    scope = class_ or module

    to_be_replaced = getattr(scope, original, None)

    if to_be_replaced is None:
        raise ConfigurationError("Original %s in %s not found" % (original, str(scope)))

    if preservedoc:
        try:
            replacement.__doc__ = to_be_replaced.__doc__
        except AttributeError:
            pass

    if docstringWarning:
        try:
            patch_warning = "\n**Monkey patched by** '%s.%s'" % (replacement.__module__, replacement.__name__)
            replacement.__doc__ += patch_warning
        except AttributeError:
            pass

    if handler is None:
        handler = _default_patch

    _context.action(
        discriminator = None,
        callable = _do_patch,
        order=order,
        args = (handler, scope, original, replacement, repr(_context.info), description)
        )


def _do_patch(handler, scope, original, replacement, zcml_info, description):
    log = logging.getLogger('collective.monkeypatcher')
    log.info("Applying monkey patch to %s : %s" % (scope, original,))
    try:
        org_dotted_name = '%s.%s.%s' %(scope.__module__, scope.__name__, original)
    except AttributeError, e:
        org_dotted_name = '%s.%s' % (scope.__name__, original)

    info = {
        'description': description,
        'zcml_info': zcml_info,
        'original': org_dotted_name,
        'replacement': '%s.%s' % (replacement.__module__, replacement.__name__)
            }

    handler(scope, original, replacement)

def _default_patch(scope, original, replacement):
    setattr(scope, original, replacement)
