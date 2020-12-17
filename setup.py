# coding: utf-8

"""
    AnonTech_Vizivault API

    A service for securely and safely managing user data  # noqa: E501

    Contact: devin.croak@anontechnology.com
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "vizivault"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "pytest>=6.1.2",
    "requests>=2.24.0"
]


setup(
    name=NAME,
    version=VERSION,
    description="Anontech Vizivault API",
    author_email="devin.croak@anontechnology.com",
    url="",
    keywords=["Nox API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    A service for securely and safely managing user data  # noqa: E501
    """
)
