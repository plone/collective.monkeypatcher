========================
collective.monkeypatcher
========================

Introduction
============

Sometimes, a monkey patch is a necessary evil.

This package makes it easier to apply a monkey patch during Zope startup.
It uses the ZCML configuration machinery to ensure that patches are loaded
"late" in the startup cycle, so that the original code has had time to be
fully initialised and configured. This is similar to using the `initialize()`
method in a product's __init__.py, except it does not require that the package
be a full-blown Zope 2 product with a persistent Control_Panel entry.

Applying a monkey patch
=======================

Here's an example::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:monkey="http://namespaces.plone.org/monkey"
        i18n_domain="collective.rooter">

        <include package="collective.monkeypatcher" file="meta.zcml" />
    
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

By default, `DocDinderTab <http://pypi.python.org/pypi/Products.DocFinderTab>`_
and other TTW API browsers will emphasize the monkey patched methods/functions,
appending the docstring with "Monkey patched with 'my.monkeypatche.function'".
If you don't want this, you could set the `docstringWarning` attribute to
`false`.


If you want to do more than just replace one function with another, you can
provide your own patcher function via the `handler` attribute. This should
be a callable like::

  def apply_patch(scope, original, replacement):
      ...

Here, `scope` is the class/module that was specified. `original` is the string
name of the function to replace, and `replacement` is the replacement function.

Handlind monkey patches events
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
