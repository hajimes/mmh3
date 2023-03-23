# MurmurHash3 was written by Austin Appleby, and is placed in the public domain.
# mmh3 Python module was written by Hajime Senuma, and is also placed in the public domain.
# The authors hereby disclaim copyright to these source codes.
import platform
import sys

from setuptools import Extension, setup

COMPILE_OPTIONS = []
LINK_OPTIONS = []


def is_new_osx():
    """Check whether we're on OSX >= 10.7"""
    if sys.platform != "darwin":
        return False
    mac_ver = platform.mac_ver()[0]
    if mac_ver.startswith("10"):
        minor_version = int(mac_ver.split(".")[1])
        return minor_version >= 7
    return False


if is_new_osx():
    # On Mac, use libc++ because Apple deprecated use of
    # libstdc
    COMPILE_OPTIONS.append("-stdlib=libc++")
    LINK_OPTIONS.append("-lc++")
    # g++ (used by unix compiler on mac) links to libstdc++ as a default lib.
    # See: https://stackoverflow.com/questions/1653047/avoid-linking-to-libstdc
    LINK_OPTIONS.append("-nodefaultlibs")

mmh3module = Extension(
    "mmh3",
    sources=["mmh3module.cpp", "MurmurHash3.cpp"],
    extra_compile_args=COMPILE_OPTIONS,
    extra_link_args=LINK_OPTIONS,
)

setup(
    name="mmh3",
    version="3.1.0",
    description="Python wrapper for MurmurHash (MurmurHash3), a set of fast and robust hash functions.",
    license="License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    author="Hajime Senuma",
    author_email="hajime.senuma@gmail.com",
    url="https://github.com/hajimes/mmh3",
    ext_modules=[mmh3module],
    keywords="utility hash MurmurHash",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
