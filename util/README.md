# Algorithm implementations used by the `mmh3` module

This directory contains C files that were generated from the
[SMHasher](https://github.com/aappleby/smhasher) C++ project by Austin Appleby.

## Updating _mmh3

Try `git submodule update --init` to fetch Appleby's original SMHasher project as a github submodule.
Then, run the `refresh.py` script to generate PEP 7-compliant C code from the original project, instead of editing `murmurhash3.*` files manually.
Add transformation code to the `refresh.py` script to perform further edits.

After file generation, use `clang-format` (with `.clang-format` in the top directory of the `mmh3` project) to format the generated code.
Try `clang-format -i src/mmh3/murmurhash3.*` from the project's top-level directory.

## Local files

1. `./README.md`
1. `./refresh.py`
1. `./FILE_HEADER`

## Generated files

1. `../src/mmh3/murmurhash3.c`
1. `../src/mmh3/murmurhash3.h`