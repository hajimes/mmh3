# MurmurHash3 was written by Austin Appleby, and is placed in the public domain.
# mmh3 Python module was written by Hajime Senuma, and is also placed in the public domain.
# The authors hereby disclaim copyright to these source codes.

from setuptools import setup, Extension

mmh3module = Extension('mmh3',
    sources = ['mmh3module.cpp', 'MurmurHash3.cpp'])

setup(name = 'mmh3',
    version = '2.4',
    description = 'Python library for MurmurHash (MurmurHash3), a set of fast and robust hash functions.',
    license = 'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    author = 'Hajime Senuma',
    author_email = 'hajime.senuma@gmail.com',
    url = 'http://packages.python.org/mmh3',
    ext_modules = [mmh3module],
    keywords = "utility hash MurmurHash",
    long_description = open('README.rst').read(),
    classifiers = ['Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities']
)
