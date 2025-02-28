from setuptools import find_packages
from setuptools import setup


version = "1.2.3.dev0"

setup(
    name="collective.monkeypatcher",
    version=version,
    description=(
        "Support for applying monkey patches late in the startup "
        "cycle by using ZCML configuration actions"
    ),
    long_description="\n".join([open("README.rst").read(), open("CHANGES.rst").read()]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.9",
    keywords="zope monkey patch",
    author="Martin Aspeli",
    author_email="optilude@gmail.com",
    url="https://github.com/plone/collective.monkeypatcher",
    license="BSD",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "six",
    ],
    extras_require={
        "test": [
            "zope.component",
            "zope.configuration",
        ],
    },
)
