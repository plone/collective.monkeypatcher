Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

2.0.0 (2025-03-21)
------------------

Breaking changes:


- Drop support for Plone 5.2 and for Python 3.8 and lower. @gforcada (#4126)


Bug fixes:


- Replace `pkg_resources` with `importlib.metadata` @gforcada @mauritsvanrees (#4126)


Internal:


- Update configuration files.
  [plone devs]


1.2.2 (2024-11-30)
------------------

Bug fixes:


- Fix removed `unittest.makeSuite` in python 3.13.
  [petschki] (#14)


1.2.1 (2020-03-21)
------------------

Bug fixes:


- Minor packaging updates. [various] (#1)


1.2 (2018-12-10)
----------------

New features:

- Include installation instructions in the README.

- Update test infrastructure.


1.1.6 (2018-10-31)
------------------

Bug fixes:

- Prepare for Python 2 / 3 compatibility
  [frapell]


1.1.5 (2018-06-18)
------------------

Bug fixes:

- Fix import for Python 3 in the tests module
  [ale-rt]


1.1.4 (2018-04-08)
------------------

Bug fixes:

- Fix import for Python 3
  [pbauer]


1.1.3 (2017-11-26)
------------------

New features:

- Document possible problems when patching module level functions
  [frisi]


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
