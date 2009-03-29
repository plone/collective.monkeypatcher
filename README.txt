Introduction
============

Sometimes, a monkey patch is a necessary evil.

This package makes it easier to apply a monkey patch during Zope startup.
It uses the ZCML configuration machinery to ensure that patches are loaded
"late" in the startup cycle, so that the original code has had time to be
fully initialised and configured. This is similar to using the `initialize()`
method in a product's __init__.py, except it does not require that the package
be a full-blown Zope 2 product with a persistent Control_Panel entry.

Here's an example::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:monkey="http://namespaces.plone.org/monkey"
        i18n_domain="collective.rooter">

        <include package="collective.monkeypatcher" file="meta.zcml" />
    
        <monkey:patch
            class="Products.CMFPlone.CatalogTool.CatalogTool"
            original="searchResults"
            replacement=".catalog.patchedSearchResults"
            />

    </configure>

In this example, we patch Plone's CatalogTool's searchResults() function,
replacing it with our own version in catalog.py. To patch a module level
function, you can use 'module' instead of 'class'. The original class and
function/method name and the replacement symbol will be checked to ensure
that they actually exist.

If patching happens too soon (or too late), use the 'order' attribute to
specify a higher (later) or lower (earlier) number. The default is 1000.