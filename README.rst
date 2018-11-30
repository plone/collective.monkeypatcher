========================
collective.monkeypatcher
========================

.. image:: https://travis-ci.com/plone/collective.monkeypatcher.svg?branch=master
    :target: https://travis-ci.com/plone/collective.monkeypatcher

.. image:: https://coveralls.io/repos/github/zopefoundation/collective.monkeypatcher/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/collective.monkeypatcher?branch=master

.. image:: https://img.shields.io/pypi/v/collective.monkeypatcher.svg
        :target: https://pypi.org/project/collective.monkeypatcher/
        :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/collective.monkeypatcher.svg
        :target: https://pypi.org/project/collective.monkeypatcher/
        :alt: Supported Python versions


Introduction
============

Sometimes, a monkey patch is a necessary evil.

This package makes it easier to apply a monkey patch during Zope startup.
It uses the ZCML configuration machinery to ensure that patches are loaded
"late" in the startup cycle, so that the original code has had time to be
fully initialised and configured. This is similar to using the `initialize()`
method in a product's __init__.py, except it does not require that the package
be a full-blown Zope product with a persistent Control_Panel entry.


Installation
============

To install `collective.monkeypatcher` into the global Python environment
(or a working environment), using a traditional Zope instance, you can do this:

* When you're reading this you have probably already run
  ``pip install collective.monkeypatcher``.

* Create a file called ``collective.monkeypatcher-configure.zcml`` in the
  ``/path/to/instance/etc/package-includes`` directory.  The file
  should only contain this::

    <include package="collective.monkeypatcher" />


Alternatively, if you are using `zc.buildout` and the
`plone.recipe.zope2instance`  recipe to manage your project, you can do this:

* Add ``collective.monkeypatcher`` to the list of eggs to install, e.g.::

    [buildout]
    ...
    eggs =
        ...
        collective.monkeypatcher

* Tell the plone.recipe.zope2instance recipe to install a ZCML slug::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        collective.monkeypatcher

* Re-run buildout, e.g. with::

    $ ./bin/buildout

You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.


Applying a monkey patch
=======================

Here's an example::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:monkey="http://namespaces.plone.org/monkey"
        i18n_domain="collective.monkeypatcher">

        <include package="collective.monkeypatcher" />

        <monkey:patch
            description="This works around issue http://some.tracker.tld/ticket/123"
            class="Products.CMFPlone.CatalogTool.CatalogTool"
            original="searchResults"
            replacement=".catalog.patchedSearchResults"
            />

    </configure>

In this example, we patch Plone's CatalogTool's searchResults() function,
replacing it with our own version in catalog.py. To patch a module level
function, you can use `module` instead of `class`. The original class and
function/method name and the replacement symbol will be checked to ensure
that they actually exist.

If patching happens too soon (or too late), use the `order` attribute to
specify a higher (later) or lower (earlier) number. The default is 1000.

By default, `DocFinderTab <http://pypi.python.org/pypi/Products.DocFinderTab>`_
and other TTW API browsers will emphasize the monkey patched methods/functions,
appending the docstring with "Monkey patched with 'my.monkeypatched.function'".
If you don't want this, you could set the `docstringWarning` attribute to
`false`.

If you want to do more than just replace one function with another, you can
provide your own patcher function via the `handler` attribute. This should
be a callable like::

  def apply_patch(scope, original, replacement):
      ...

Here, `scope` is the class/module that was specified. `original` is the string
name of the function to replace, and `replacement` is the replacement function.

Full list of options:

- ``class``  The class being patched
- ``module`` The module being patched (see `Patching module level functions`_)
- ``handler`` A function to perform the patching. Must take three parameters: class/module, original (string), and replacement
- ``original`` Method or function to replace
- ``replacement`` Method or function to replace with
- ``preservedoc`` Preserve docstrings?
- ``preserveOriginal`` Preserve the original function so that it is reachable view prefix _old_. Only works for default handler
- ``preconditions`` Preconditions (multiple, separated by space) to be satisified before applying this patch. Example: Products.LinguaPlone-=1.4.3 or Products.TextIndexNG3+=3.3.0
- ``ignoreOriginal`` Ignore if the orginal function isn't present on the class/module being patched
- ``docstringWarning``  Add monkey patch warning in docstring
- ``description``  Some comments about your monkey patch
- ``order`` Execution order

Handling monkey patches events
==============================

Applying a monkey patch fires an event. See the `interfaces.py` module. If you
to handle such event add this ZCML bunch::

  ...
  <subscriber
    for="collective.monkeypatcher.interfaces.IMonkeyPatchEvent"
    handler="my.component.events.myHandler"
    />
  ...

And add such Python::

  def myHandler(event):
      """see collective.monkeypatcher.interfaces.IMonkeyPatchEvent"""
      ...


Patching module level functions
===============================


.. ATTENTION:: Be aware that patching module level functions will likely not work.


If you want to patch the method `do_something` located in `patched.package.utils` which is imported in a package like this

::

    from patched.package.utils import do_something

the reference to this function is loaded *before* `collective.monkeypatcher` will patch the original method.

See also `this related thread on the plone mailing list <http://plone.293351.n2.nabble.com/Monkey-Patch-Module-Level-td7557725.html>`_.

Workaround
----------


Do the patching in `__init__.py` of your package::

    from patched.package import utils

    def do_it_different():
        return 'foo'

    utils.do_something = do_it_different
