// To handle 64-bit data; see https://docs.python.org/3/c-api/arg.html
#ifndef PY_SSIZE_T_CLEAN
#define PY_SSIZE_T_CLEAN
#endif

#include <Python.h>
#include <stdio.h>
#include <string.h>

#include "hashlib.h"
#include "murmurhash3.h"

#if defined(_MSC_VER)
typedef signed __int8 int8_t;
typedef signed __int32 int32_t;
typedef signed __int64 int64_t;
typedef unsigned __int8 uint8_t;
typedef unsigned __int32 uint32_t;
typedef unsigned __int64 uint64_t;
// Other compilers
#else  // defined(_MSC_VER)
#include <stdint.h>
#endif  // defined(_MSC_VER)

#define MMH3S_DIGESTSIZE 8

PyDoc_STRVAR(mmh3_hash_doc,
             "hash(key[, seed=0, signed=True]) -> 32-bit int\n\n"
             "Return a hash value as a 32-bit integer. "
             "Calculated by the MurmurHash3_x86_32 algorithm.");

static PyObject *
mmh3_hash(PyObject *self, PyObject *args, PyObject *keywds)
{
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

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#|IB", kwlist,
                                     &target_str, &target_str_len, &seed,
                                     &is_signed)) {
        return NULL;
    }

    murmurhash3_x86_32(target_str, target_str_len, seed, result);

#if defined(_MSC_VER)
    /* for Windows envs */
    long_result = result[0];
    if (is_signed == 1) {
        return PyLong_FromLong(long_result);
    }
    else {
        return PyLong_FromUnsignedLong(long_result);
    }
#else  // defined(_MSC_VER)
    /* for standard envs */
#if __LONG_WIDTH__ == 64 || defined(__APPLE__)
    long_result = result[0] & mask[is_signed];
    return PyLong_FromLong(long_result);
#else   // __LONG_WIDTH__ == 64 || defined(__APPLE__)
    long_result = result[0];
    if (is_signed == 1) {
        return PyLong_FromLong(long_result);
    }
    else {
        return PyLong_FromUnsignedLong(long_result);
    }
#endif  // __LONG_WIDTH__ == 64 || defined(__APPLE__)
#endif  // defined(_MSC_VER)
}

PyDoc_STRVAR(mmh3_hash_from_buffer_doc,
             "hash_from_buffer(key[, seed=0, signed=True]) -> 32-bit int\n\n"
             "Return a hash value from a memory buffer as a 32-bit integer. "
             "Calculated by the MurmurHash3_x86_32 algorithm. "
             "Designed for large memory-views such as numpy arrays.");

static PyObject *
mmh3_hash_from_buffer(PyObject *self, PyObject *args, PyObject *keywds)
{
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

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s*|IB", kwlist,
                                     &target_buf, &seed, &is_signed)) {
        return NULL;
    }

    murmurhash3_x86_32(target_buf.buf, target_buf.len, seed, result);

#if defined(_MSC_VER)
    /* for Windows envs */
    long_result = result[0];
    if (is_signed == 1) {
        return PyLong_FromLong(long_result);
    }
    else {
        return PyLong_FromUnsignedLong(long_result);
    }
#else  // defined(_MSC_VER)
/* for standard envs */
#if __LONG_WIDTH__ == 64 || defined(__APPLE__)
    long_result = result[0] & mask[is_signed];
    return PyLong_FromLong(long_result);
#else   // __LONG_WIDTH__ == 64 || defined(__APPLE__)
    long_result = result[0];
    if (is_signed == 1) {
        return PyLong_FromLong(long_result);
    }
    else {
        return PyLong_FromUnsignedLong(long_result);
    }
#endif  // __LONG_WIDTH__ == 64 || defined(__APPLE__)
#endif  // defined(_MSC_VER)
}

PyDoc_STRVAR(
    mmh3_hash64_doc,
    "hash64(key[, seed=0, x64arch=True, signed=True]) -> (64-bit int, 64-bit "
    "int)\n\n"
    "Return a tuple of two 64 bit integers given an input string. "
    "Calculated by the MurmurHash3_x{64, 86}_128 algorithm. Optimized "
    "for the x64 bit architecture when x64arch=True, otherwise for x86.");

static PyObject *
mmh3_hash64(PyObject *self, PyObject *args, PyObject *keywds)
{
    const char *target_str;
    Py_ssize_t target_str_len;
    uint32_t seed = 0;
    uint64_t result[2];
    char x64arch = 1;
    int is_signed = 1;

    static char *kwlist[] = {(char *)"key", (char *)"seed", (char *)"x64arch",
                             (char *)"signed", NULL};

    static char *valflag[] = {(char *)"KK", (char *)"LL"};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#|IBB", kwlist,
                                     &target_str, &target_str_len, &seed,
                                     &x64arch, &is_signed)) {
        return NULL;
    }

    if (x64arch == 1) {
        murmurhash3_x64_128(target_str, target_str_len, seed, result);
    }
    else {
        murmurhash3_x86_128(target_str, target_str_len, seed, result);
    }

    PyObject *retval = Py_BuildValue(valflag[is_signed], result[0], result[1]);
    return retval;
}

PyDoc_STRVAR(
    mmh3_hash128_doc,
    "hash128(key[, seed=0, x64arch=True, signed=False]]) -> 128-bit int\n\n"
    "Return a 128 bit long integer. "
    "Calculated by the MurmurHash3_x{64, 86}_128 algorithm. "
    "Optimized for the x64 bit architecture "
    "when x64arch=True, otherwise for x86.");

static PyObject *
mmh3_hash128(PyObject *self, PyObject *args, PyObject *keywds)
{
    const char *target_str;
    Py_ssize_t target_str_len;
    uint32_t seed = 0;
    uint64_t result[2];
    char x64arch = 1;
    char is_signed = 0;

    static char *kwlist[] = {(char *)"key", (char *)"seed", (char *)"x64arch",
                             (char *)"signed", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#|IBB", kwlist,
                                     &target_str, &target_str_len, &seed,
                                     &x64arch, &is_signed)) {
        return NULL;
    }

    if (x64arch == 1) {
        murmurhash3_x64_128(target_str, target_str_len, seed, result);
    }
    else {
        murmurhash3_x86_128(target_str, target_str_len, seed, result);
    }

    /**
     * _PyLong_FromByteArray is not a part of the official Python/C API
     * and may be removed in the future (although it is practically stable).
     * cf.
     * https://mail.python.org/pipermail/python-list/2006-August/372365.html
     */
    PyObject *retval =
        _PyLong_FromByteArray((unsigned char *)result, 16, 1, is_signed);

    return retval;
}

PyDoc_STRVAR(
    mmh3_hash_bytes_doc,
    "hash_bytes(key[, seed=0, x64arch=True]) -> bytes\n\n"
    "Return a 128 bit hash value as bytes for a string. Optimized for "
    "the x64 bit architecture when "
    "x64arch=True, otherwise for the x86.");

static PyObject *
mmh3_hash_bytes(PyObject *self, PyObject *args, PyObject *keywds)
{
    const char *target_str;
    Py_ssize_t target_str_len;
    uint32_t seed = 0;
    uint32_t result[4];
    char x64arch = 1;

    static char *kwlist[] = {(char *)"key", (char *)"seed", (char *)"x64arch",
                             NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#|IB", kwlist,
                                     &target_str, &target_str_len, &seed,
                                     &x64arch)) {
        return NULL;
    }

    if (x64arch == 1) {
        murmurhash3_x64_128(target_str, target_str_len, seed, result);
    }
    else {
        murmurhash3_x86_128(target_str, target_str_len, seed, result);
    }

    char bytes[16];
    memcpy(bytes, result, 16);
    return PyBytes_FromStringAndSize(bytes, 16);
}

// The design of hasher classes are loosely based on the Google Guava
// implementation (Java)
typedef struct {
    PyObject_HEAD uint32_t h;
    uint64_t buffer;
    uint32_t shift;
    Py_ssize_t length;
} Hasher32;

static void
Hasher32_dealloc(Hasher32 *self)
{
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
Hasher32_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Hasher32 *self;
    self = (Hasher32 *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->h = 0;
        self->buffer = 0;
        self->shift = 0;
        self->length = 0;
    }
    return (PyObject *)self;
}

static int
Hasher32_init(Hasher32 *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"seed", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|I", kwlist, &self->h))
        return -1;

    return 0;
}

static PyObject *
Hasher32_update(Hasher32 *self, PyObject *obj)
{
    Py_ssize_t i = 0;
    Py_buffer buf;
    uint32_t h1 = self->h;
    uint32_t k1 = 0;
    const uint64_t mask = 0xffffffffL;

    GET_BUFFER_VIEW_OR_ERROUT(obj, &buf);

    for (; i + 4 <= buf.len; i += 4) {
        k1 = getblock32(buf.buf, i / 4);
        self->buffer |= (k1 & mask) << self->shift;
        self->length += 4;

        h1 = mixH1(h1, mixK1(self->buffer));
        self->buffer >>= 32;
    }

    for (; i < buf.len; i++) {
        k1 = ((uint8_t *)buf.buf)[i];
        self->buffer |= (k1 & mask) << self->shift;
        self->shift += 8;
        self->length += 1;

        if (self->shift >= 32) {
            h1 = mixH1(h1, mixK1(self->buffer));
            self->buffer >>= 32;
            self->shift -= 32;
        }
    }

    PyBuffer_Release(&buf);

    self->h = h1;

    Py_RETURN_NONE;
}

static FORCE_INLINE uint32_t
digest32_impl(uint32_t h, uint64_t k1, Py_ssize_t length)
{
    h ^= mixK1(k1);
    h ^= length;
    h = fmix32(h);
    return h;
}

static PyObject *
Hasher32_sintdigest(Hasher32 *self, PyObject *Py_UNUSED(ignored))
{
    uint32_t h = digest32_impl(self->h, self->buffer, self->length);

    // Note that simple casting ("(int32_t) h") is an undefined behavior
    int32_t result = *(int32_t *)&h;

    return PyLong_FromLong(result);
}

static PyObject *
Hasher32_uintdigest(Hasher32 *self, PyObject *Py_UNUSED(ignored))
{
    uint32_t h = digest32_impl(self->h, self->buffer, self->length);
    return PyLong_FromUnsignedLong(h);
}

static PyMethodDef Hasher32_methods[] = {
    {"sintdigest", (PyCFunction)Hasher32_sintdigest, METH_NOARGS, "doc here"},
    {"uintdigest", (PyCFunction)Hasher32_uintdigest, METH_NOARGS, "doc here"},
    {"update", (PyCFunction)Hasher32_update, METH_O, "doc here"},
    {NULL} /* Sentinel */
};

static PyObject *
Hasher32_get_digest_size(PyObject *self, void *closure)
{
    return PyLong_FromLong(MMH3S_DIGESTSIZE);
}

static PyGetSetDef Hasher32_getsetters[] = {
    {"digest_size", (getter)Hasher32_get_digest_size, NULL, NULL, NULL},
    {NULL} /* Sentinel */
};

static PyTypeObject Hasher32Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "mmh3.mmh3_32",
    .tp_doc = PyDoc_STR("MMH3_32"),
    .tp_basicsize = sizeof(Hasher32),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Hasher32_new,
    .tp_init = (initproc)Hasher32_init,
    .tp_dealloc = (destructor)Hasher32_dealloc,
    .tp_methods = Hasher32_methods,
    .tp_getset = Hasher32_getsetters,
};

struct module_state {
    PyObject *error;
};

#define GETSTATE(m) ((struct module_state *)PyModule_GetState(m))

static PyMethodDef Mmh3Methods[] = {
    {"hash", (PyCFunctionWithKeywords)mmh3_hash, METH_VARARGS | METH_KEYWORDS,
     mmh3_hash_doc},
    {"hash_from_buffer", (PyCFunction)mmh3_hash_from_buffer,
     METH_VARARGS | METH_KEYWORDS, mmh3_hash_from_buffer_doc},
    {"hash64", (PyCFunctionWithKeywords)mmh3_hash64,
     METH_VARARGS | METH_KEYWORDS, mmh3_hash64_doc},
    {"hash128", (PyCFunctionWithKeywords)mmh3_hash128,
     METH_VARARGS | METH_KEYWORDS, mmh3_hash128_doc},
    {"hash_bytes", (PyCFunctionWithKeywords)mmh3_hash_bytes,
     METH_VARARGS | METH_KEYWORDS, mmh3_hash_bytes_doc},
    {NULL, NULL, 0, NULL}};

static int
mmh3_traverse(PyObject *m, visitproc visit, void *arg)
{
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int
mmh3_clear(PyObject *m)
{
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}

static struct PyModuleDef mmh3module = {
    PyModuleDef_HEAD_INIT,
    "mmh3",
    PyDoc_STR(
        "mmh3 is a Python front-end to MurmurHash3, "
        "a fast and robust hash library "
        "created by Austin Appleby (http://code.google.com/p/smhasher/).\n "
        "Ported by Hajime Senuma <hajime.senuma@gmail.com>\n"
        "Try hash('foobar') or hash('foobar', 1984).\n"
        "If you find any bugs, please submit an issue via "
        "https://github.com/hajimes/mmh3"),
    sizeof(struct module_state),
    Mmh3Methods,
    NULL,
    mmh3_traverse,
    mmh3_clear,
    NULL};

// HASHLIB_GIL_MINSIZE
// Py_BEGIN_ALLOW_THREADS

PyMODINIT_FUNC
PyInit_mmh3(void)
{
    if (PyType_Ready(&Hasher32Type) < 0)
        return NULL;

    PyObject *module = PyModule_Create(&mmh3module);

    if (module == NULL)
        return NULL;

    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException((char *)"mmh3.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&Hasher32Type);
    if (PyModule_AddObject(module, "mmh3_32", (PyObject *)&Hasher32Type) < 0) {
        Py_DECREF(&Hasher32Type);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}