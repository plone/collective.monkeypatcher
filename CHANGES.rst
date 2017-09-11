Changelog
=========

1.1.3 (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- Document possible problems when patching module level functions
  [frisi]

Bug fixes:

- *add item here*


1.1.2 (2016-08-10)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


1.1.1 (2015-03-27)
------------------

- Fix typo.
  [gforcada]


1.1 - 2014-12-10
----------------

* Fix the case where the replacement object does not have a __module__
  attribute (see https://github.com/plone/collective.monkeypatcher/pull/3).
  [mitchellrj, fRiSi]

1.0.1 - 2011-01-25
------------------

* Downgrade standard log message to debug level.
  [hannosch]

1.0 - 2010-07-01
----------------

* Avoid a zope.app dependency.
  [hannosch]

* Added new parameter preconditions that only patches if preconditions are met
  like version of a specific package.
  [spamsch]

* Added new parameter preserveOriginal. Setting this to true makes it possible
  to access the patched method via _old_``name of patched method``
  [spamsch]

1.0b2 - 2009-06-18
------------------

* Add the possibility to ignore the error if the original function isn't
  present on the class/module being patched
  [jfroche]

* Check if the docstring exists before changing it
  [jfroche]

* Add buildout.cfg for test & test coverage
  [jfroche]

1.0b1 - 2009-04-17
------------------

* Fires an event when a monkey patch is applied. See interfaces.py.
  [glenfant]

* Added ZCML attributes "docstringWarning" and "description".
  [glenfant]

* Added unit tests.
  [glenfant]

1.0a1 - 2009-03-29
------------------

* Initial release
  [optilude]
