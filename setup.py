# -*- coding: utf-8 -*-
# -*- mode: python -*-
import os
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

VERSION = '0.3.0'
cls_txt = """
Development Status :: 3 - Alpha
Framework :: Django
Intended Audience :: Science/Research
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Dynamic Content
"""

setup(
    name="django-lab-inventory",
    version=VERSION,
    description="A simple Django app for managing lab inventory",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    classifiers=[x for x in cls_txt.split("\n") if x],
    author='C Daniel Meliza',
    author_email='dan@meliza@org',
    maintainer='C Daniel Meliza',
    maintainer_email='dan@meliza.org',
    url = "https://github.com/melizalab/django-lab-inventory",
    packages=['inventory'],
    include_package_data=True,
)
