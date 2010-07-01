# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.0.1'

setup(name='collective.monkeypatcher',
      version=version,
      description="Support for applying monkey patches late in the startup cycle by using ZCML configuration actions",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='zope monkey patch',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://pypi.python.org/pypi/collective.monkeypatcher',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      )
