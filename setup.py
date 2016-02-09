# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '1.1.2.dev0'

setup(
    name='collective.monkeypatcher',
    version=version,
    description=("Support for applying monkey patches late in the startup "
                 "cycle by using ZCML configuration actions"),
    long_description='\n'.join([
        open("README.rst").read(),
        open("CHANGES.rst").read()]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        ],
    keywords='zope monkey patch',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='https://pypi.python.org/pypi/collective.monkeypatcher',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    )
