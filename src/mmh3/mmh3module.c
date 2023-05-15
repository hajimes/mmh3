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

#define MMH3_32_DIGESTSIZE 4
#define MMH3_128_DIGESTSIZE 16

#define MMH3_32_BLOCKSIZE 12
#define MMH3_128_BLOCKSIZE 32

//-----------------------------------------------------------------------------
// One shot functions

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

    char bytes[MMH3_128_DIGESTSIZE];
    memcpy(bytes, result, MMH3_128_DIGESTSIZE);
    return PyBytes_FromStringAndSize(bytes, MMH3_128_DIGESTSIZE);
}

static PyMethodDef Mmh3Methods[] = {
    {"hash", (PyCFunction)mmh3_hash, METH_VARARGS | METH_KEYWORDS,
     mmh3_hash_doc},
    {"hash_from_buffer", (PyCFunction)mmh3_hash_from_buffer,
     METH_VARARGS | METH_KEYWORDS, mmh3_hash_from_buffer_doc},
    {"hash64", (PyCFunction)mmh3_hash64, METH_VARARGS | METH_KEYWORDS,
     mmh3_hash64_doc},
    {"hash128", (PyCFunction)mmh3_hash128, METH_VARARGS | METH_KEYWORDS,
     mmh3_hash128_doc},
    {"hash_bytes", (PyCFunction)mmh3_hash_bytes, METH_VARARGS | METH_KEYWORDS,
     mmh3_hash_bytes_doc},
    {NULL, NULL, 0, NULL}};

//-----------------------------------------------------------------------------
// Hasher classes
//
// The design of hasher classes are loosely based on the Google Guava
// implementation (Java)

//-----------------------------------------------------------------------------
// Hasher for murmurhash3_x86_32
typedef struct {
    PyObject_HEAD uint32_t h;
    uint64_t buffer;
    uint8_t shift;
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
    const uint32_t c1 = 0xe6546b64;
    const uint64_t mask = 0xffffffffUL;

    GET_BUFFER_VIEW_OR_ERROUT(obj, &buf);

    for (; i + 4 <= buf.len; i += 4) {
        k1 = getblock32(buf.buf, i / 4);
        self->buffer |= (k1 & mask) << self->shift;
        self->length += 4;

        h1 ^= mixK1(self->buffer);
        h1 = mixH1(h1, 0, 13, c1);
        self->buffer >>= 32;
    }

    for (; i < buf.len; i++) {
        k1 = ((uint8_t *)buf.buf)[i];
        self->buffer |= (k1 & mask) << self->shift;
        self->shift += 8;
        self->length += 1;

        if (self->shift >= 32) {
            h1 ^= mixK1(self->buffer);
            h1 = mixH1(h1, 0, 13, c1);
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
Hasher32_digest(Hasher32 *self, PyObject *Py_UNUSED(ignored))
{
    uint32_t h = digest32_impl(self->h, self->buffer, self->length);
    char out[MMH3_32_DIGESTSIZE];
    ((uint32_t *)out)[0] = h;
    return PyBytes_FromStringAndSize(out, MMH3_32_DIGESTSIZE);
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
    {"digest", (PyCFunction)Hasher32_digest, METH_NOARGS, "doc here"},
    {"sintdigest", (PyCFunction)Hasher32_sintdigest, METH_NOARGS, "doc here"},
    {"uintdigest", (PyCFunction)Hasher32_uintdigest, METH_NOARGS, "doc here"},
    {"update", (PyCFunction)Hasher32_update, METH_O, "doc here"},
    {NULL} /* Sentinel */
};

static PyObject *
Hasher32_get_digest_size(PyObject *self, void *closure)
{
    return PyLong_FromLong(MMH3_32_DIGESTSIZE);
}

static PyObject *
Hasher32_get_block_size(PyObject *self, void *closure)
{
    return PyLong_FromLong(MMH3_32_BLOCKSIZE);
}

static PyObject *
Hasher32_get_name(PyObject *self, void *closure)
{
    return PyUnicode_FromStringAndSize("mmh3_32", 7);
}

static PyGetSetDef Hasher32_getsetters[] = {
    {"digest_size", (getter)Hasher32_get_digest_size, NULL, NULL, NULL},
    {"block_size", (getter)Hasher32_get_block_size, NULL, NULL, NULL},
    {"name", (getter)Hasher32_get_name, NULL, NULL, NULL},
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

//-----------------------------------------------------------------------------
// Hasher for murmurhash3_x64_128
typedef struct {
    PyObject_HEAD uint64_t h1;
    uint64_t h2;
    uint64_t buffer1;
    uint64_t buffer2;
    uint8_t shift;
    Py_ssize_t length;
} Hasher128;

static void
Hasher128x64_dealloc(Hasher128 *self)
{
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
Hasher128x64_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Hasher128 *self;
    self = (Hasher128 *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->h1 = 0;
        self->h2 = 0;
        self->buffer1 = 0;
        self->buffer2 = 0;
        self->shift = 0;
        self->length = 0;
    }
    return (PyObject *)self;
}

static int
Hasher128x64_init(Hasher128 *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"seed", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|I", kwlist, &self->h1))
        return -1;

    self->h2 = self->h1;

    return 0;
}

static PyObject *
Hasher128x64_update(Hasher128 *self, PyObject *obj)
{
    Py_ssize_t i = 0;
    Py_buffer buf;
    uint64_t h1 = self->h1;
    uint64_t h2 = self->h2;
    uint64_t k1 = 0;
    uint64_t k2 = 0;

    GET_BUFFER_VIEW_OR_ERROUT(obj, &buf);

    for (; i + 16 <= buf.len; i += 16) {
        k1 = getblock64(buf.buf, (i / 16) * 2);
        k2 = getblock64(buf.buf, (i / 16) * 2 + 1);

        if (self->shift == 0) {  // TODO: use bit ops
            self->buffer1 = k1;
            self->buffer2 = k2;
        }
        else if (self->shift < 64) {
            self->buffer1 |= k1 << self->shift;
            self->buffer2 = (k1 >> (64 - self->shift)) | (k2 << self->shift);
        }
        else if (self->shift == 64) {
            self->buffer2 = k1;
        }
        else {
            self->buffer2 |= k1 << (self->shift - 64);
        }

        h1 ^= mixK1_x64_128(self->buffer1);
        h1 = mixH_x64_128(h1, h2, 27, 0x52dce729UL);
        h2 ^= mixK2_x64_128(self->buffer2);
        h2 = mixH_x64_128(h2, h1, 31, 0x38495ab5UL);

        self->length += 16;
        if (self->shift == 0) {  // TODO: use bit ops
            self->buffer1 = 0;
            self->buffer2 = 0;
        }
        else if (self->shift < 64) {
            self->buffer1 = k2 >> (64 - self->shift);
            self->buffer2 = 0;
        }
        else if (self->shift == 64) {
            self->buffer1 = k2;
            self->buffer2 = 0;
        }
        else {
            self->buffer1 =
                k1 >> (128 - self->shift) | (k2 << (self->shift - 64));
            self->buffer2 = k2 >> (128 - self->shift);
        }
    }

    for (; i < buf.len; i++) {
        k1 = ((uint8_t *)buf.buf)[i];
        if (self->shift < 64) {  // TODO: use bit ops
            self->buffer1 |= k1 << self->shift;
        }
        else {
            self->buffer2 |= k1 << (self->shift - 64);
        }
        self->shift += 8;
        self->length += 1;

        if (self->shift >= 128) {
            h1 ^= mixK1_x64_128(self->buffer1);
            h1 = mixH_x64_128(h1, h2, 27, 0x52dce729UL);
            h2 ^= mixK2_x64_128(self->buffer2);
            h2 = mixH_x64_128(h2, h1, 31, 0x38495ab5UL);

            self->buffer1 = 0;
            self->buffer2 = 0;
            self->shift -= 128;
        }
    }

    PyBuffer_Release(&buf);

    self->h1 = h1;
    self->h2 = h2;

    Py_RETURN_NONE;
}

static PyObject *
Hasher128x64_digest(Hasher128 *self, PyObject *Py_UNUSED(ignored))
{
    const char out[MMH3_128_DIGESTSIZE];
    digest_x64_128_impl(self->h1, self->h2, self->buffer1, self->buffer2,
                        self->length, out);
    return PyBytes_FromStringAndSize(out, MMH3_128_DIGESTSIZE);
}

static PyObject *
Hasher128x64_sintdigest(Hasher128 *self, PyObject *Py_UNUSED(ignored))
{
    const char out[MMH3_128_DIGESTSIZE];
    digest_x64_128_impl(self->h1, self->h2, self->buffer1, self->buffer2,
                        self->length, out);
    const int little_endian = 1;
    const int is_signed = 1;

    /**
     * _PyLong_FromByteArray is not a part of the official Python/C API
     * and may be removed in the future (although it is practically stable).
     * cf.
     * https://mail.python.org/pipermail/python-list/2006-August/372365.html
     */
    PyObject *retval = _PyLong_FromByteArray(
        (unsigned char *)out, MMH3_128_DIGESTSIZE, little_endian, is_signed);

    return retval;
}

static PyObject *
Hasher128x64_uintdigest(Hasher128 *self, PyObject *Py_UNUSED(ignored))
{
    const char out[MMH3_128_DIGESTSIZE];
    digest_x64_128_impl(self->h1, self->h2, self->buffer1, self->buffer2,
                        self->length, out);
    const int little_endian = 1;
    const int is_signed = 0;

    /**
     * _PyLong_FromByteArray is not a part of the official Python/C API
     * and may be removed in the future (although it is practically stable).
     * cf.
     * https://mail.python.org/pipermail/python-list/2006-August/372365.html
     */
    PyObject *retval = _PyLong_FromByteArray(
        (unsigned char *)out, MMH3_128_DIGESTSIZE, little_endian, is_signed);

    return retval;
}

static PyObject *
Hasher128x64_stupledigest(Hasher128 *self, PyObject *Py_UNUSED(ignored))
{
    const char out[MMH3_128_DIGESTSIZE];
    digest_x64_128_impl(self->h1, self->h2, self->buffer1, self->buffer2,
                        self->length, out);

    char *valflag = "LL";
    PyObject *retval =
        Py_BuildValue(valflag, ((uint64_t *)out)[0], ((uint64_t *)out)[1]);

    return retval;
}

static PyObject *
Hasher128x64_utupledigest(Hasher128 *self, PyObject *Py_UNUSED(ignored))
{
    const char out[MMH3_128_DIGESTSIZE];
    digest_x64_128_impl(self->h1, self->h2, self->buffer1, self->buffer2,
                        self->length, out);

    char *valflag = "KK";
    PyObject *retval =
        Py_BuildValue(valflag, ((uint64_t *)out)[0], ((uint64_t *)out)[1]);

    return retval;
}

static PyMethodDef Hasher128x64_methods[] = {
    {"digest", (PyCFunction)Hasher128x64_digest, METH_NOARGS, "doc here"},
    {"sintdigest", (PyCFunction)Hasher128x64_sintdigest, METH_NOARGS,
     "doc here"},
    {"uintdigest", (PyCFunction)Hasher128x64_uintdigest, METH_NOARGS,
     "doc here"},
    {"stupledigest", (PyCFunction)Hasher128x64_stupledigest, METH_NOARGS,
     "doc here"},
    {"utupledigest", (PyCFunction)Hasher128x64_utupledigest, METH_NOARGS,
     "doc here"},
    {"update", (PyCFunction)Hasher128x64_update, METH_O, "doc here"},
    {NULL} /* Sentinel */
};

static PyObject *
Hasher128x64_get_digest_size(PyObject *self, void *closure)
{
    return PyLong_FromLong(MMH3_128_DIGESTSIZE);
}

static PyObject *
Hasher128x64_get_block_size(PyObject *self, void *closure)
{
    return PyLong_FromLong(MMH3_128_BLOCKSIZE);
}

static PyObject *
Hasher128x64_get_name(PyObject *self, void *closure)
{
    return PyUnicode_FromStringAndSize("mmh3_x64_128", 12);
}

static PyGetSetDef Hasher128x64_getsetters[] = {
    {"digest_size", (getter)Hasher128x64_get_digest_size, NULL, NULL, NULL},
    {"block_size", (getter)Hasher128x64_get_block_size, NULL, NULL, NULL},
    {"name", (getter)Hasher128x64_get_name, NULL, NULL, NULL},
    {NULL} /* Sentinel */
};

static PyTypeObject Hasher128Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "mmh3.mmh3_x64_128",
    .tp_doc = PyDoc_STR("MMH3_X64_128"),
    .tp_basicsize = sizeof(Hasher128),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Hasher128x64_new,
    .tp_init = (initproc)Hasher128x64_init,
    .tp_dealloc = (destructor)Hasher128x64_dealloc,
    .tp_methods = Hasher128x64_methods,
    .tp_getset = Hasher128x64_getsetters,
};

//-----------------------------------------------------------------------------
// Hasher for murmurhash3_x86_128
typedef struct {
    PyObject_HEAD uint32_t h1;
    uint32_t h2;
    uint32_t h3;
    uint32_t h4;
    uint32_t buffer1;
    uint32_t buffer2;
    uint32_t buffer3;
    uint32_t buffer4;
    uint8_t shift;
    Py_ssize_t length;
} Hasher128x86;

static void
Hasher128x86_dealloc(Hasher128x86 *self)
{
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
Hasher128x86_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Hasher128x86 *self;
    self = (Hasher128x86 *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->h1 = 0;
        self->h2 = 0;
        self->h3 = 0;
        self->h4 = 0;
        self->buffer1 = 0;
        self->buffer2 = 0;
        self->buffer3 = 0;
        self->buffer4 = 0;
        self->shift = 0;
        self->length = 0;
    }
    return (PyObject *)self;
}

static int
Hasher128x86_init(Hasher128x86 *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"seed", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|I", kwlist, &self->h1))
        return -1;

    self->h2 = self->h1;
    self->h3 = self->h1;
    self->h4 = self->h1;

    return 0;
}

static PyObject *
Hasher128x86_update(Hasher128x86 *self, PyObject *obj)
{
    Py_ssize_t i = 0;
    Py_buffer buf;
    uint32_t h1 = self->h1;
    uint32_t h2 = self->h2;
    uint32_t h3 = self->h3;
    uint32_t h4 = self->h4;
    uint32_t k1 = 0;
    uint32_t k2 = 0;
    uint32_t k3 = 0;
    uint32_t k4 = 0;

    GET_BUFFER_VIEW_OR_ERROUT(obj, &buf);

    for (; i < buf.len; i++) {
        k1 = ((uint8_t *)buf.buf)[i];
        if (self->shift < 32) {  // TODO: use bit ops
            self->buffer1 |= k1 << self->shift;
        }
        else if (self->shift < 64) {
            self->buffer2 |= k1 << (self->shift - 32);
        }
        else if (self->shift < 96) {
            self->buffer3 |= k1 << (self->shift - 64);
        }
        else {
            self->buffer4 |= k1 << (self->shift - 96);
        }
        self->shift += 8;
        self->length += 1;

        if (self->shift >= 128) {
            const uint32_t c1 = 0x239b961b;
            const uint32_t c2 = 0xab0e9789;
            const uint32_t c3 = 0x38b34ae5;
            const uint32_t c4 = 0xa1e38b93;

            h1 ^= mixK_x86_128(self->buffer1, 15, c1, c2);
            h1 = mixH1(h1, h2, 19, 0x561ccd1bUL);

            h2 ^= mixK_x86_128(self->buffer2, 16, c2, c3);
            h2 = mixH1(h2, h3, 17, 0x0bcaa747UL);

            h3 ^= mixK_x86_128(self->buffer3, 17, c3, c4);
            h3 = mixH1(h3, h4, 15, 0x96cd1c35UL);

            h4 ^= mixK_x86_128(self->buffer4, 18, c4, c1);
            h4 = mixH1(h4, h1, 13, 0x32ac3b17UL);

            self->buffer1 = 0;
            self->buffer2 = 0;
            self->buffer3 = 0;
            self->buffer4 = 0;
            self->shift -= 128;
        }
    }

    PyBuffer_Release(&buf);

    self->h1 = h1;
    self->h2 = h2;
    self->h3 = h3;
    self->h4 = h4;

    Py_RETURN_NONE;
}

static PyObject *
Hasher128x86_digest(Hasher128x86 *self, PyObject *Py_UNUSED(ignored))
{
    char out[MMH3_128_DIGESTSIZE];
    digest_x86_128_impl(self->h1, self->h2, self->h3, self->h4, self->buffer1,
                        self->buffer2, self->buffer3, self->buffer4,
                        self->length, out);
    return PyBytes_FromStringAndSize(out, MMH3_128_DIGESTSIZE);
}

static PyObject *
Hasher128x86_sintdigest(Hasher128x86 *self, PyObject *Py_UNUSED(ignored))
{
    const char out[MMH3_128_DIGESTSIZE];
    digest_x86_128_impl(self->h1, self->h2, self->h3, self->h4, self->buffer1,
                        self->buffer2, self->buffer3, self->buffer4,
                        self->length, out);
    const int little_endian = 1;
    const int is_signed = 1;

    /**
     * _PyLong_FromByteArray is not a part of the official Python/C API
     * and may be removed in the future (although it is practically stable).
     * cf.
     * https://mail.python.org/pipermail/python-list/2006-August/372365.html
     */
    PyObject *retval = _PyLong_FromByteArray(
        (unsigned char *)out, MMH3_128_DIGESTSIZE, little_endian, is_signed);

    return retval;
}

static PyObject *
Hasher128x86_uintdigest(Hasher128x86 *self, PyObject *Py_UNUSED(ignored))
{
    const char out[MMH3_128_DIGESTSIZE];
    digest_x86_128_impl(self->h1, self->h2, self->h3, self->h4, self->buffer1,
                        self->buffer2, self->buffer3, self->buffer4,
                        self->length, out);
    const int little_endian = 1;
    const int is_signed = 0;

    /**
     * _PyLong_FromByteArray is not a part of the official Python/C API
     * and may be removed in the future (although it is practically stable).
     * cf.
     * https://mail.python.org/pipermail/python-list/2006-August/372365.html
     */
    PyObject *retval = _PyLong_FromByteArray(
        (unsigned char *)out, MMH3_128_DIGESTSIZE, little_endian, is_signed);

    return retval;
}

static PyObject *
Hasher128x86_stupledigest(Hasher128x86 *self, PyObject *Py_UNUSED(ignored))
{
    const char out[MMH3_128_DIGESTSIZE];
    digest_x86_128_impl(self->h1, self->h2, self->h3, self->h4, self->buffer1,
                        self->buffer2, self->buffer3, self->buffer4,
                        self->length, out);

    char *valflag = "LL";
    PyObject *retval =
        Py_BuildValue(valflag, ((uint64_t *)out)[0], ((uint64_t *)out)[1]);

    return retval;
}

static PyObject *
Hasher128x86_utupledigest(Hasher128x86 *self, PyObject *Py_UNUSED(ignored))
{
    const char out[MMH3_128_DIGESTSIZE];
    digest_x86_128_impl(self->h1, self->h2, self->h3, self->h4, self->buffer1,
                        self->buffer2, self->buffer3, self->buffer4,
                        self->length, out);

    char *valflag = "KK";
    PyObject *retval =
        Py_BuildValue(valflag, ((uint64_t *)out)[0], ((uint64_t *)out)[1]);

    return retval;
}

static PyMethodDef Hasher128x86_methods[] = {
    {"digest", (PyCFunction)Hasher128x86_digest, METH_NOARGS, "doc here"},
    {"sintdigest", (PyCFunction)Hasher128x86_sintdigest, METH_NOARGS,
     "doc here"},
    {"uintdigest", (PyCFunction)Hasher128x86_uintdigest, METH_NOARGS,
     "doc here"},
    {"stupledigest", (PyCFunction)Hasher128x86_stupledigest, METH_NOARGS,
     "doc here"},
    {"utupledigest", (PyCFunction)Hasher128x86_utupledigest, METH_NOARGS,
     "doc here"},
    {"update", (PyCFunction)Hasher128x86_update, METH_O, "doc here"},
    {NULL} /* Sentinel */
};

static PyObject *
Hasher128x86_get_digest_size(PyObject *self, void *closure)
{
    return PyLong_FromLong(MMH3_128_DIGESTSIZE);
}

static PyObject *
Hasher128x86_get_block_size(PyObject *self, void *closure)
{
    return PyLong_FromLong(MMH3_128_BLOCKSIZE);
}

static PyObject *
Hasher128x86_get_name(PyObject *self, void *closure)
{
    return PyUnicode_FromStringAndSize("mmh3_x86_128", 12);
}

static PyGetSetDef Hasher128x86_getsetters[] = {
    {"digest_size", (getter)Hasher128x86_get_digest_size, NULL, NULL, NULL},
    {"block_size", (getter)Hasher128x86_get_block_size, NULL, NULL, NULL},
    {"name", (getter)Hasher128x86_get_name, NULL, NULL, NULL},
    {NULL} /* Sentinel */
};

static PyTypeObject Hasher128x86Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "mmh3.mmh3_x86_128",
    .tp_doc = PyDoc_STR("MMH3_X86_128"),
    .tp_basicsize = sizeof(Hasher128x86),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Hasher128x86_new,
    .tp_init = (initproc)Hasher128x86_init,
    .tp_dealloc = (destructor)Hasher128x86_dealloc,
    .tp_methods = Hasher128x86_methods,
    .tp_getset = Hasher128x86_getsetters,
};

//-----------------------------------------------------------------------------
// Module
static struct PyModuleDef mmh3module = {
    PyModuleDef_HEAD_INIT,
    "mmh3",
    "mmh3 is a Python front-end to MurmurHash3, "
    "a fast and robust hash library "
    "created by Austin Appleby (http://code.google.com/p/smhasher/).\n "
    "Ported by Hajime Senuma <hajime.senuma@gmail.com>\n"
    "Try hash('foobar') or hash('foobar', 1984).\n"
    "If you find any bugs, please submit an issue via "
    "https://github.com/hajimes/mmh3",
    -1,
    Mmh3Methods,
    NULL,
    NULL,
    NULL,
    NULL};

PyMODINIT_FUNC
PyInit_mmh3(void)
{
    if (PyType_Ready(&Hasher32Type) < 0)
        return NULL;

    if (PyType_Ready(&Hasher128Type) < 0)
        return NULL;

    if (PyType_Ready(&Hasher128x86Type) < 0)
        return NULL;

    PyObject *module = PyModule_Create(&mmh3module);

    if (module == NULL)
        return NULL;

    Py_INCREF(&Hasher32Type);
    if (PyModule_AddObject(module, "mmh3_32", (PyObject *)&Hasher32Type) < 0) {
        Py_DECREF(&Hasher32Type);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&Hasher128Type);
    if (PyModule_AddObject(module, "mmh3_x64_128",
                           (PyObject *)&Hasher128Type) < 0) {
        Py_DECREF(&Hasher128Type);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&Hasher128x86Type);
    if (PyModule_AddObject(module, "mmh3_x86_128",
                           (PyObject *)&Hasher128x86Type) < 0) {
        Py_DECREF(&Hasher128x86Type);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}