//-----------------------------------------------------------------------------
// MurmurHash3 was written by Austin Appleby, and is placed in the public
// domain. mmh3 Python module was written by Hajime Senuma,
// and is also placed in the public domain/CC0 1.0.
// The authors hereby disclaim copyright to these source codes.

// To handle 64-bit data; see https://docs.python.org/3/c-api/arg.html
#ifndef PY_SSIZE_T_CLEAN
#define PY_SSIZE_T_CLEAN
#endif

#include "MurmurHash3.h"
#include <Python.h>
#include <stdio.h>
#include <string.h>

#if defined(_MSC_VER)
typedef signed __int8 int8_t;
typedef signed __int32 int32_t;
typedef signed __int64 int64_t;
typedef unsigned __int8 uint8_t;
typedef unsigned __int32 uint32_t;
typedef unsigned __int64 uint64_t;
// Other compilers
#else // defined(_MSC_VER)
#include <stdint.h>
#endif // defined(_MSC_VER)

static PyObject *mmh3_hash(PyObject *self, PyObject *args, PyObject *keywds) {
  const char *target_str;
  Py_ssize_t target_str_len;
  uint32_t seed = 0;
  int32_t result[1];
  long long_result = 0;
  int is_signed = 1;

  static char *kwlist[] = {(char *)"key", (char *)"seed", (char *)"signed",
                           NULL};

#ifndef _MSC_VER
#if __LONG_WIDTH__ == 64 || defined(__APPLE__)
  static uint64_t mask[] = {0x0ffffffff, 0xffffffffffffffff};
#endif
#endif

  if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#|IB", kwlist, &target_str,
                                   &target_str_len, &seed, &is_signed)) {
    return NULL;
  }

  MurmurHash3_x86_32(target_str, target_str_len, seed, result);

#if defined(_MSC_VER)
  /* for Windows envs */
  long_result = result[0];
  if (is_signed == 1) {
    return PyLong_FromLong(long_result);
  } else {
    return PyLong_FromUnsignedLong(long_result);
  }
#else // defined(_MSC_VER)
  /* for standard envs */
#if __LONG_WIDTH__ == 64 || defined(__APPLE__)
  long_result = result[0] & mask[is_signed];
  return PyLong_FromLong(long_result);
#else  // __LONG_WIDTH__ == 64 || defined(__APPLE__)
  long_result = result[0];
  if (is_signed == 1) {
    return PyLong_FromLong(long_result);
  } else {
    return PyLong_FromUnsignedLong(long_result);
  }
#endif // __LONG_WIDTH__ == 64 || defined(__APPLE__)
#endif // defined(_MSC_VER)
}

static PyObject *mmh3_hash_from_buffer(PyObject *self, PyObject *args,
                                       PyObject *keywds) {
  Py_buffer target_buf;
  uint32_t seed = 0;
  int32_t result[1];
  long long_result = 0;
  int is_signed = 1;

  static char *kwlist[] = {(char *)"key", (char *)"seed", (char *)"signed",
                           NULL};

#ifndef _MSC_VER
#if __LONG_WIDTH__ == 64 || defined(__APPLE__)
  static uint64_t mask[] = {0x0ffffffff, 0xffffffffffffffff};
#endif
#endif

  if (!PyArg_ParseTupleAndKeywords(args, keywds, "s*|IB", kwlist, &target_buf,
                                   &seed, &is_signed)) {
    return NULL;
  }

  MurmurHash3_x86_32(target_buf.buf, target_buf.len, seed, result);

#if defined(_MSC_VER)
  /* for Windows envs */
  long_result = result[0];
  if (is_signed == 1) {
    return PyLong_FromLong(long_result);
  } else {
    return PyLong_FromUnsignedLong(long_result);
  }
#else // defined(_MSC_VER)
/* for standard envs */
#if __LONG_WIDTH__ == 64 || defined(__APPLE__)
  long_result = result[0] & mask[is_signed];
  return PyLong_FromLong(long_result);
#else  // __LONG_WIDTH__ == 64 || defined(__APPLE__)
  long_result = result[0];
  if (is_signed == 1) {
    return PyLong_FromLong(long_result);
  } else {
    return PyLong_FromUnsignedLong(long_result);
  }
#endif // __LONG_WIDTH__ == 64 || defined(__APPLE__)
#endif // defined(_MSC_VER)
}

static PyObject *mmh3_hash64(PyObject *self, PyObject *args, PyObject *keywds) {
  const char *target_str;
  Py_ssize_t target_str_len;
  uint32_t seed = 0;
  uint64_t result[2];
  char x64arch = 1;
  int is_signed = 1;

  static char *kwlist[] = {(char *)"key", (char *)"seed", (char *)"x64arch",
                           (char *)"signed", NULL};

  static char *valflag[] = {(char *)"KK", (char *)"LL"};

  if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#|IBB", kwlist, &target_str,
                                   &target_str_len, &seed, &x64arch,
                                   &is_signed)) {
    return NULL;
  }

  if (x64arch == 1) {
    MurmurHash3_x64_128(target_str, target_str_len, seed, result);
  } else {
    MurmurHash3_x86_128(target_str, target_str_len, seed, result);
  }

  PyObject *retval = Py_BuildValue(valflag[is_signed], result[0], result[1]);
  return retval;
}

static PyObject *mmh3_hash128(PyObject *self, PyObject *args,
                              PyObject *keywds) {
  const char *target_str;
  Py_ssize_t target_str_len;
  uint32_t seed = 0;
  uint64_t result[2];
  char x64arch = 1;
  char is_signed = 0;

  static char *kwlist[] = {(char *)"key", (char *)"seed", (char *)"x64arch",
                           (char *)"signed", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#|IBB", kwlist, &target_str,
                                   &target_str_len, &seed, &x64arch,
                                   &is_signed)) {
    return NULL;
  }

  if (x64arch == 1) {
    MurmurHash3_x64_128(target_str, target_str_len, seed, result);
  } else {
    MurmurHash3_x86_128(target_str, target_str_len, seed, result);
  }

  /**
   * _PyLong_FromByteArray is not a part of the official Python/C API
   * and may be removed in the future (although it is practically stable).
   * cf. https://mail.python.org/pipermail/python-list/2006-August/372365.html
   */
  PyObject *retval =
      _PyLong_FromByteArray((unsigned char *)result, 16, 1, is_signed);

  return retval;
}

static PyObject *mmh3_hash_bytes(PyObject *self, PyObject *args,
                                 PyObject *keywds) {
  const char *target_str;
  Py_ssize_t target_str_len;
  uint32_t seed = 0;
  uint32_t result[4];
  char x64arch = 1;

  static char *kwlist[] = {(char *)"key", (char *)"seed", (char *)"x64arch",
                           NULL};

  if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#|IB", kwlist, &target_str,
                                   &target_str_len, &seed, &x64arch)) {
    return NULL;
  }

  if (x64arch == 1) {
    MurmurHash3_x64_128(target_str, target_str_len, seed, result);
  } else {
    MurmurHash3_x86_128(target_str, target_str_len, seed, result);
  }

  char bytes[16];
  memcpy(bytes, result, 16);
  return PyBytes_FromStringAndSize(bytes, 16);
}

struct module_state {
  PyObject *error;
};

#define GETSTATE(m) ((struct module_state *)PyModule_GetState(m))

static PyMethodDef Mmh3Methods[] = {
    {"hash", (PyCFunction)mmh3_hash, METH_VARARGS | METH_KEYWORDS,
     "hash(key[, seed=0, signed=True]) -> hash value\n Return a 32 bit "
     "integer."},
    {"hash_from_buffer", (PyCFunction)mmh3_hash_from_buffer,
     METH_VARARGS | METH_KEYWORDS,
     "hash_from_buffer(key[, seed=0, signed=True]) -> hash value from a memory "
     "buffer\n Return a 32 bit integer. Designed for large memory-views such "
     "as numpy arrays."},
    {"hash64", (PyCFunction)mmh3_hash64, METH_VARARGS | METH_KEYWORDS,
     "hash64(key[, seed=0, x64arch=True, signed=True]) -> (hash value 1, hash "
     "value 2)\n Return a tuple of two 64 bit integers for a string. Optimized "
     "for the x64 bit architecture when x64arch=True, otherwise for x86."},
    {"hash128", (PyCFunction)mmh3_hash128, METH_VARARGS | METH_KEYWORDS,
     "hash128(key[, seed=0, x64arch=True, signed=False]]) -> hash value\n "
     "Return a 128 bit long integer. Optimized for the x64 bit architecture "
     "when x64arch=True, otherwise for x86."},
    {"hash_bytes", (PyCFunction)mmh3_hash_bytes, METH_VARARGS | METH_KEYWORDS,
     "hash_bytes(key[, seed=0, x64arch=True]) -> bytes\n Return a 128 bit hash "
     "value as bytes for a string. Optimized for the x64 bit architecture when "
     "x64arch=True, otherwise for the x86."},
    {NULL, NULL, 0, NULL}};

static int mmh3_traverse(PyObject *m, visitproc visit, void *arg) {
  Py_VISIT(GETSTATE(m)->error);
  return 0;
}

static int mmh3_clear(PyObject *m) {
  Py_CLEAR(GETSTATE(m)->error);
  return 0;
}

static struct PyModuleDef mmh3module = {
    PyModuleDef_HEAD_INIT,
    "mmh3",
    "mmh3 is a Python front-end to MurmurHash3, a fast and robust hash library "
    "created by Austin Appleby (http://code.google.com/p/smhasher/).\n Ported "
    "by Hajime Senuma <hajime.senuma@gmail.com>\n Try hash('foobar') or "
    "hash('foobar', 1984).\n If you find any bugs, please submit an issue via "
    "https://github.com/hajimes/mmh3",
    sizeof(struct module_state),
    Mmh3Methods,
    NULL,
    mmh3_traverse,
    mmh3_clear,
    NULL};

#define INITERROR return NULL

extern "C" {
PyMODINIT_FUNC PyInit_mmh3(void)

{
  PyObject *module = PyModule_Create(&mmh3module);

  if (module == NULL)
    INITERROR;

  PyModule_AddStringConstant(module, "__version__", "3.1.0");

  struct module_state *st = GETSTATE(module);

  st->error = PyErr_NewException((char *)"mmh3.Error", NULL, NULL);
  if (st->error == NULL) {
    Py_DECREF(module);
    INITERROR;
  }

  return module;
}
} // extern "C"