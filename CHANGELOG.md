# Changelog

All notable changes to this project will be documented here. For a list of
contributors, see the
[Contributors](https://mmh3.readthedocs.io/en/stable/CONTRIBUTORS.html) page.

The format is based on
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
This project has adhered to
[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)
since version 3.0.0.

## [5.2.0] - 2025-07-29

### Added

- Add support for Python 3.14, including 3.14t (no-GIL) wheels. However, thread
  safety for the no-GIL variant is not fully tested yet. Please report any
  issues you encounter ([#134](https://github.com/hajimes/mmh3/pull/134),
  [#136](https://github.com/hajimes/mmh3/pull/136)).
- Add support for Android (Python 3.13 only) and iOS (Python 3.13 and 3.14) wheels,
  enabled by the major version update of
  [cibuildwheel](https://github.com/pypa/cibuildwheel)
  ([#135](https://github.com/hajimes/mmh3/pull/135)).

## [5.1.0] - 2025-01-25

### Added

- Improve the performance of `hash128()`, `hash64()`, and `hash_bytes()` by
  using
  [METH_FASTCALL](https://docs.python.org/3/c-api/structures.html#c.METH_FASTCALL),
  reducing the overhead of function calls
  ([#116](https://github.com/hajimes/mmh3/pull/116)).
- Add the software paper for this library
  ([doi:10.21105/joss.06124](https://doi.org/10.21105/joss.06124)), following
  its publication in the
  [_Journal of Open Source Software_](https://joss.theoj.org)
  ([#118](https://github.com/hajimes/mmh3/pull/118)).

### Removed

- Drop support for Python 3.8, as it has reached the end of life on 2024-10-07
  ([#117](https://github.com/hajimes/mmh3/pull/117)).

## [5.0.1] - 2024-09-22

### Fixed

- Fix the issue that the package cannot be built from the source distribution
  ([#90](https://github.com/hajimes/mmh3/issues/90)).

## [5.0.0] - 2024-09-18

### Added

- Add support for Python 3.13.
- Improve the performance of the `hash()` function with
  [METH_FASTCALL](https://docs.python.org/3/c-api/structures.html#c.METH_FASTCALL),
  reducing the overhead of function calls. For data sizes between 1–2 KB
  (e.g., 48x48 favicons), performance is 10%–20% faster. For smaller data
  (~500 bytes, like 16x16 favicons), performance increases by approximately 30%
  ([#87](https://github.com/hajimes/mmh3/pull/87)).
- Add `digest` functions that support the new buffer protocol
  ([PEP 688](https://peps.python.org/pep-0688/)) as input
  ([#75](https://github.com/hajimes/mmh3/pull/75)).
  These functions are implemented with `METH_FASTCALL` too, offering improved
  performance ([#84](https://github.com/hajimes/mmh3/pull/84)).
- Slightly improve the performance of the `hash_bytes()` function
  ([#88](https://github.com/hajimes/mmh3/pull/88))
- Add Read the Docs documentation
  ([#54](https://github.com/hajimes/mmh3/issues/54)).
- Document benchmark results
  ([#53](https://github.com/hajimes/mmh3/issues/53)).

### Changed

- **Backward-incompatible**: The `seed` argument is now strictly validated to
  ensure it falls within the range [0, 0xFFFFFFFF]. A `ValueError` is raised
  if the seed is out of range ([#84](https://github.com/hajimes/mmh3/pull/84)).
- **Backward-incompatible**: Change the constructors of hasher classes to
  accept a buffer as the first argument
  ([#83](https://github.com/hajimes/mmh3/pull/83)).
- The type of flag argumens has been changed from `bool` to `Any`
  ([#84](https://github.com/hajimes/mmh3/pull/84)).
- Change the format of CHANGELOG.md to conform to the
  [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) standard
  ([#63](https://github.com/hajimes/mmh3/pull/63)).

### Deprecated

- Deprecate the `hash_from_buffer()` function.
  Use `mmh3_32_sintdigest()` or `mmh3_32_uintdigest()` as alternatives
  ([#84](https://github.com/hajimes/mmh3/pull/84)).

### Fixed

- Fix a reference leak in the `hash_from_buffer()` function
  ([#75](https://github.com/hajimes/mmh3/pull/75)).
- Fix type hints ([#76](https://github.com/hajimes/mmh3/pull/76),
  [#77](https://github.com/hajimes/mmh3/pull/77),
  [#84](https://github.com/hajimes/mmh3/pull/84)).

## [4.1.0] - 2024-01-09

### Added

- Add support for Python 3.12.

### Fixed

- Fix issues with Bazel by changing the directory structure of the project
  ([#50](https://github.com/hajimes/mmh3/issues/50)).
- Fix incorrect type hints ([#51](https://github.com/hajimes/mmh3/issues/51)).
- Fix invalid results on s390x when the arg `x64arch` of `hash64` or
  `hash_bytes()` is set to `False`
  ([#52](https://github.com/hajimes/mmh3/issues/52)).

## [4.0.1] - 2023-07-14

### Changed

- Refactor the project structure
  ([#48](https://github.com/hajimes/mmh3/issues/48)).

### Fixed

- Fix incorrect type hints.

## [4.0.0] - 2023-05-22

### Added

- Add experimental support for `hashlib`-compliant hasher classes
  ([#39](https://github.com/hajimes/mmh3/issues/39)). Note that they are not yet
  fully tuned for performance.
- Add support for type hints ([#44](https://github.com/hajimes/mmh3/issues/44)).
- Add wheels for more platforms (`musllinux`, `s390x`, `win_arm64`, and
  `macosx_universal2`).
- Add a code of conduct (the ACM Code of Ethics and Professional Conduct).

### Changed

- Switch license from CC0 to MIT
  ([#43](https://github.com/hajimes/mmh3/issues/43)).

### Removed

- **Backward-incompatible**: A hash function now returns the same value under
  big-endian platforms as that under little-endian ones
  ([#47](https://github.com/hajimes/mmh3/issues/47)).
- **Backward-incompatible**: Remove the `__version__` constant from the module
  ([#42](https://github.com/hajimes/mmh3/issues/42)). Use `importlib.metadata`
  instead.
- Drop support for Python 3.7, as it will reach the end of life on 2023-06-27.

## [3.1.0] - 2023-03-24

### Added

- Add support for Python 3.10 and 3.11
  ([#35](https://github.com/hajimes/mmh3/pull/35),
  [#37](https://github.com/hajimes/mmh3/pull/37)).
- Add support for 32-bit architectures such as `i686` and `armv7l`. From now on,
  `hash()` and `hash_from_buffer()` on these architectures will generate the
  same hash values as those on other environments
  ([#40](https://github.com/hajimes/mmh3/pull/40)).
- In relation to the above, `manylinux2014_i686` wheels are now available.
- Support for hashing huge data (>16GB)
  ([#34](https://github.com/hajimes/mmh3/pull/34)).

### Removed

- Drop support for Python 3.6; remove legacy code for Python 2.x at the source
  code level.

## [3.0.0] - 2021-02-23

### Added

- Python wheels are now available, thanks to the power of
  [cibuildwheel](https://github.com/joerick/cibuildwheel).
  - Supported platforms are `manylinux1_x86_64`, `manylinux2010_x86_64`,
    `manylinux2014_aarch64`, `win32`, `win_amd64`, `macosx_10_9_x86_64`, and
    `macosx_11_0_arm64` (Apple Silicon).
- Add support for newer macOS environments
  ([#22](https://github.com/hajimes/mmh3/pull/22)).
- Add support for Python 3.7, 3.8, and 3.9.

### Changed

- Migrate CI from Travis CI and AppVeyor to GitHub Actions.

### Removed

- Drop support for Python 2.7, 3.3, 3.4, and 3.5.

## [2.5.1] - 2017-10-31

### Fixed

- Bugfix for `hash_bytes()` ([#15](https://github.com/hajimes/mmh3/pull/15)).

## [2.5] - 2017-10-28

### Added

- Add `hash_from_buffer()` ([#13](https://github.com/hajimes/mmh3/pull/13)).
- Add a keyword argument `signed`.

## [2.4] - 2017-05-27

### Added

- Support seeds with 32-bit unsigned integers
  ([#6](https://github.com/hajimes/mmh3/pull/6)).
- Support 64-bit data (under 64-bit environments)
- Add unit testing and continuous integration with Travis CI and AppVeyor.

### Fixed

- Fix compile errors for Python 3.6 under Windows systems.

## [2.3.2] - 2017-05-26

### Changed

- Relicensed from public domain to CC0-1.0.

## [2.3.1] - 2015-06-07

### Fixed

- Fix compile errors for gcc >=5.

## [2.3] - 2013-12-08

### Added

- Add `hash128()`, which returns a 128-bit signed integer
  ([#3](https://github.com/hajimes/mmh3/pull/3)).

### Fixed

- Fix a misplaced operator which could cause memory leak in a rare condition
  ([#2](https://github.com/hajimes/mmh3/pull/2)).
- Fix a malformed value to a Python/C API function which may cause runtime
  errors in recent Python 3.x versions.

## [2.2] - 2013-03-03

### Added

- Improve portability to support systems with old gcc (version < 4.4) such as
  CentOS/RHEL 5.x
  ([#1](https://github.com/hajimes/mmh3/pull/1)).

## [2.1] - 2013-02-25

### Added

- Add `__version__` constant. Check if it exists when the following revision
  matters for your application.

### Changed

- Incorporate the revision r147, which includes robustness improvement and minor
  tweaks.

Beware that due to this revision, **the result of 32-bit version of 2.1 is NOT
the same as that of 2.0**. E.g.,:

```pycon
>>> mmh3.hash("foo") # in mmh3 2.0
-292180858
>>> mmh3.hash("foo") # in mmh3 2.1
-156908512
```

The results of hash64 and hash_bytes remain unchanged. Austin Appleby, the
author of Murmurhash, ensured this revision was the final modification to
MurmurHash3's results and any future changes would be to improve performance
only.

## [2.0] - 2011-06-07

### Added

- Support both Python 2.7 and 3.x.

### Changed

- Change the module interface.

## [1.0] - 2011-04-27

### Added

- As
  [Softpedia collected mmh3 1.0 on April 27, 2011](https://web.archive.org/web/20110430172027/https://linux.softpedia.com/get/Programming/Libraries/mmh3-68314.shtml),
  it must have been uploaded to PyPI on or slightly before this date.

[5.2.0]: https://github.com/hajimes/mmh3/compare/v5.1.0...v5.2.0
[5.1.0]: https://github.com/hajimes/mmh3/compare/v5.0.1...v5.1.0
[5.0.1]: https://github.com/hajimes/mmh3/compare/v5.0.0...v5.0.1
[5.0.0]: https://github.com/hajimes/mmh3/compare/v4.1.0...v5.0.0
[4.1.0]: https://github.com/hajimes/mmh3/compare/v4.0.1...v4.1.0
[4.0.1]: https://github.com/hajimes/mmh3/compare/v4.0.0...v4.0.1
[4.0.0]: https://github.com/hajimes/mmh3/compare/v3.1.0...v4.0.0
[3.1.0]: https://github.com/hajimes/mmh3/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/hajimes/mmh3/compare/v2.5.1...v3.0.0
[2.5.1]: https://github.com/hajimes/mmh3/compare/v2.5...v2.5.1
[2.5]: https://github.com/hajimes/mmh3/compare/v2.4...v2.5
[2.4]: https://github.com/hajimes/mmh3/compare/v2.3.2...v2.4
[2.3.2]: https://github.com/hajimes/mmh3/compare/v2.3.1...v2.3.2
[2.3.1]: https://github.com/hajimes/mmh3/compare/v2.3...v2.3.1
[2.3]: https://github.com/hajimes/mmh3/compare/v2.2...v2.3
[2.2]: https://github.com/hajimes/mmh3/compare/v2.1...v2.2
[2.1]: https://github.com/hajimes/mmh3/compare/v2.0...v2.1
[2.0]: https://github.com/hajimes/mmh3/releases/tag/v2.0
[1.0]: https://web.archive.org/web/20110430172027/https://linux.softpedia.com/get/Programming/Libraries/mmh3-68314.shtml
