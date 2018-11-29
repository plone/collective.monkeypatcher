# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '1.1.7.dev0'

setup(
    name='collective.monkeypatcher',
    version=version,
    description=("Support for applying monkey patches late in the startup "
                 "cycle by using ZCML configuration actions"),
    long_description='\n'.join([
        open("README.rst").read(),
        open("CHANGES.rst").read()]),
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        ],
    keywords='zope monkey patch',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='https://github.com/plone/collective.monkeypatcher',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'six',
    ],
    )
