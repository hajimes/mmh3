/***
 * This file is under MIT <year> Hajime Senuma, just like other files.
 * See LICENSE for details.
 *
 * It was originally written by Austin Appleby in C++ under the public domain,
 * but ported to PEP 7 C for Python 3.6 and later by the mmh3 project.
 *
 * Any issues should be reported to https://github.com/hajimes/mmh3/issues.
 *
 * The following is the original public domain notice by Austin Appleby.
 */

//-----------------------------------------------------------------------------
// MurmurHash3 was written by Austin Appleby, and is placed in the public
// domain. The author hereby disclaims copyright to this source code.

#ifndef MURMURHASH3_H_
#define MURMURHASH3_H_

// To handle 64-bit data; see https://docs.python.org/3/c-api/arg.html
#ifndef PY_SSIZE_T_CLEAN
#define PY_SSIZE_T_CLEAN
#endif
#include <Python.h>

//-----------------------------------------------------------------------------
// Platform-specific functions and macros

// Microsoft Visual Studio

#if defined(_MSC_VER)
typedef unsigned __int8 uint8_t;
typedef unsigned __int32 uint32_t;
typedef unsigned __int64 uint64_t;

// Other compilers

#else  // defined(_MSC_VER)

#include <stdint.h>

#endif  // !defined(_MSC_VER)

//-----------------------------------------------------------------------------

void
murmurhash3_x86_32(const void *key, Py_ssize_t len, uint32_t seed, void *out);

void
murmurhash3_x86_128(const void *key, Py_ssize_t len, uint32_t seed, void *out);

void
murmurhash3_x64_128(const void *key, Py_ssize_t len, uint32_t seed, void *out);

//-----------------------------------------------------------------------------

#endif  // MURMURHASH3_H_