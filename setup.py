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
    "attrs==20.2.0",
    "certifi==2019.11.28",
    "chardet==3.0.4",
    "idna==2.10",
    "importlib-metadata==2.0.0",
    "iniconfig==1.1.1",
    "jsonobject==0.9.9",
    "packaging==20.4",
    "pluggy==0.13.1",
    "py==1.9.0",
    "pyparsing==2.4.7",
    "pytest==6.1.2",
    "python-dateutil==2.8.1",
    "requests==2.24.0",
    "six==1.15.0",
    "toml==0.10.2",
    "urllib3==1.25.11",
    "zipp==3.4.0"
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
