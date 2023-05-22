# Changelog
## 4.0.0 (2023-05-22)
* Add experimental support for `hashlib`-compliant hasher classes (<https://github.com/hajimes/mmh3/issues/39>). Note that they are not yet fully tuned for performance.
* Add support for type hints (<https://github.com/hajimes/mmh3/issues/44>).
* Add wheels for more platforms (`musllinux`, `s390x`, `win_arm64`, and `macosx_universal2`).
* Drop support for Python 3.7, as it will reach the end of life on 2023-06-27.
* Switch license from CC0 to MIT (<https://github.com/hajimes/mmh3/issues/43>).
* Add a code of conduct (the ACM Code of Ethics and Professional Conduct).
* Backward incompatible changes:
  * A hash function now returns the same value under big-endian platforms as that under little-endian ones (<https://github.com/hajimes/mmh3/issues/47>).
  * Remove the `__version__` constant from the module (<https://github.com/hajimes/mmh3/issues/42>). Use `importlib.metadata` instead.

## 3.1.0 (2023-03-24)
* Add support for Python 3.10 and 3.11. Thanks [wouter bolsterlee](https://github.com/wbolster) and [Dušan Nikolić](https://github.com/n-dusan)!
* Drop support for Python 3.6; remove legacy code for Python 2.x at the source code level.
* Add support for 32-bit architectures such as `i686` and `armv7l`. From now on, `hash` and `hash_from_buffer` on these architectures will generate the same hash values as those on other environments. Thanks [Danil Shein](https://github.com/dshein-alt)!
* In relation to the above, `manylinux2014_i686` wheels are now available.
* Support for hashing huge data (>16GB). Thanks [arieleizenberg](https://github.com/arieleizenberg)!

## 3.0.0 (2021-02-23)
* Python wheels are now available, thanks to the power of [cibuildwheel](https://github.com/joerick/cibuildwheel).
  * Supported platforms are `manylinux1_x86_64`, `manylinux2010_x86_64`, `manylinux2014_aarch64`, `win32`, `win_amd64`, `macosx_10_9_x86_64`, and `macosx_11_0_arm64` (Apple Silicon).
* Add support for newer macOS environments. Thanks [Matthew Honnibal](https://github.com/honnibal)!
* Drop support for Python 2.7, 3.3, 3.4, and 3.5.
* Add support for Python 3.7, 3.8, and 3.9.
* Migrate CI from Travis CI and AppVeyor to GitHub Actions.

## 2.5.1 (2017-10-31)
* Bugfix for `hash_bytes`. Thanks [doozr](https://github.com/doozr)!

## 2.5 (2017-10-28)
* Add `hash_from_buffer`. Thanks [Dimitri Vorona](https://github.com/alendit)!
* Add a keyword argument `signed`.

## 2.4 (2017-05-27)
* Support seeds with 32-bit unsigned integers; thanks [Alexander Maznev](https://github.com/pik)!
* Support 64-bit data (under 64-bit environments)
* Fix compile errors for Python 3.6 under Windows systems.
* Add unit testing and continuous integration with Travis CI and AppVeyor.

## 2.3.2 (2017-05-26)
* Relicensed from public domain to [CC0-1.0](./LICENSE).

## 2.3.1 (2015-06-07)
* Fix compile errors for gcc >=5.

## 2.3 (2013-12-08)
* Add `hash128`, which returns a 128-bit signed integer.
* Fix a misplaced operator which could cause memory leak in a rare condition.
* Fix a malformed value to a Python/C API function which may cause runtime errors in recent Python 3.x versions.

The first two commits are from [Derek Wilson](https://github.com/underrun). Thanks!

## 2.2 (2013-03-03)
* Improve portability to support systems with old gcc (version < 4.4) such as CentOS/RHEL 5.x. (Commit from [Micha Gorelick](https://github.com/mynameisfiber). Thanks!)

## 2.1 (2013-02-25)
* Add `__version__` constant. Check if it exists when the following revision matters for your application.
* Incorporate the revision r147, which includes robustness improvement and minor tweaks.

Beware that due to this revision, **the result of 32-bit version of 2.1 is NOT the same as that of 2.0**. E.g.,:

```shell
>>> mmh3.hash("foo") # in mmh3 2.0
-292180858
>>> mmh3.hash("foo") # in mmh3 2.1
-156908512
```

The results of hash64 and hash_bytes remain unchanged. Austin Appleby, the author of Murmurhash, ensured this revision was the final modification to MurmurHash3's results and any future changes would be to improve performance only.

## 2.0 (2011-06-07)
* Support both Python 2.7 and 3.x.
* Change the module interface.

## 1.0 (<= 2011-04-27)
* As [Softpedia collected mmh3 1.0 on April 27, 2011](https://web.archive.org/web/20110430172027/https://linux.softpedia.com/get/Programming/Libraries/mmh3-68314.shtml), it must have been uploaded to PyPI on or slightly before this date.