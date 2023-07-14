from __future__ import annotations

import os
import re
import textwrap
from collections.abc import Callable

###
# Simple classes to handle the transformation of the original code.
#


class MMH3Source:
    """A data class to represent the original source code of MurmurHash3.

    Lines to be retrieved are hard-coded, as the original code is effectively frozen.
    """

    def __init__(self, code: str) -> None:
        self._code_lines = code.split("\n")

    @property
    def note_comment(self) -> str:
        return "\n".join(self._code_lines[4:8])

    @property
    def header_include(self) -> str:
        return "\n".join(self._code_lines[9:10])

    @property
    def macros(self) -> str:
        return "\n".join(self._code_lines[11:50])

    @property
    def getblock_functions(self) -> str:
        return "\n".join(self._code_lines[50:64])

    @property
    def finalization_mixes(self) -> str:
        return "\n".join(self._code_lines[64:91])

    @property
    def body(self) -> str:
        return "\n".join(self._code_lines[91:336])

    @property
    def finalization_x86_128(self) -> str:
        return "\n".join(self._code_lines[233:246])

    @property
    def finalization_x64_128(self) -> str:
        return "\n".join(self._code_lines[318:329])

    @property
    def constants_x86_128(self) -> str:
        return "\n".join(self._code_lines[160:164])

    @property
    def constants_x64_128(self) -> str:
        return "\n".join(self._code_lines[263:265])


class MMH3Header:
    """A data class to represent the original header code of MurmurHash3.

    Lines to be retrieved are hard-coded, as the original code is effectively frozen.
    """

    def __init__(self, code: str) -> None:
        self._code_lines = code.split("\n")

    @property
    def header_guards_begin(self) -> str:
        return "\n".join(self._code_lines[4:7])

    @property
    def stdint(self) -> str:
        return "\n".join(self._code_lines[7:26])

    @property
    def declarations(self) -> str:
        return "\n".join(self._code_lines[26:36])

    @property
    def header_guards_end(self) -> str:
        return "\n".join(self._code_lines[36:37])


class MMH3CodeBuilder:
    def __init__(self) -> None:
        self._code: list[tuple[str, list[Callable[[str], str]]]] = []

    def add(
        self, subcode: str, transforms: list[Callable[[str], str]] = []
    ) -> MMH3CodeBuilder:
        self._code.append((subcode, transforms))
        return self

    def build(self) -> str:
        new_code = ""

        for subcode, transforms in self._code:
            for tr in transforms:
                subcode = tr(subcode)
            new_code += subcode + "\n\n"

        return new_code


###
# The following functions are used to transform the original MurmurHash3 code.
#


def append_python_directives(subcode: str) -> str:
    """Append Python.h, as well as a macro definition to handle 64-bit data.

    Args:
        subcode (str): The code to be appended.

    Returns:
        str: The appended code.
    """
    subcode += "\n\n"

    subcode += textwrap.dedent(
        """\
        // To handle 64-bit data; see https://docs.python.org/3/c-api/arg.html
        #ifndef PY_SSIZE_T_CLEAN
        #define PY_SSIZE_T_CLEAN
        #endif
        #include <Python.h>
        """
    )

    return subcode


def append_byteswap_header(subcode: str) -> str:
    """Append a header to the code that includes byteswap.h if the system is big endian.

    Args:
        subcode (str): The code to be appended.

    Returns:
        str: The appended code.
    """
    subcode += "\n"

    subcode += textwrap.dedent(
        """\
        #if defined(__BYTE_ORDER__) && (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
        #include <byteswap.h>
        #endif
        """
    )

    return subcode


def introduce_py_ssize_t(subcode: str) -> str:
    """Use Py_ssize_t instead of int as the index type.

    Py_ssize_t is the type used by Python to represent the size of objects.
    It is required to handle 64-bit data in Python extentions.

    See https://docs.python.org/3/c-api/intro.html#c.Py_ssize_t
    and
    https://peps.python.org/pep-0353/

    Args:
        subcode (str): The code to be transformed.

    Returns:
        str: The transformed code.
    """
    transformations = [
        ["int len", "Py_ssize_t len"],
        ["const int nblocks", "const Py_ssize_t nblocks"],
        ["for(int i", "for(Py_ssize_t i"],
    ]

    for tr in transformations:
        subcode = subcode.replace(tr[0], tr[1])

    return subcode


def transform_getblocks(subcode: str) -> str:
    """Revise getblock functions so that it handles big endian and 64-bit data.

    Args:
        subcode (str): The code to be transformed.

    Returns:
        str: The transformed code.
    """

    transformations = [
        ["FORCE_INLINE", "static FORCE_INLINE"],
        ["int i", "Py_ssize_t i"],
    ]

    for tr in transformations:
        subcode = subcode.replace(tr[0], tr[1])

    BYTE_SWAP_IF_BIG_ENDIAN = textwrap.dedent(
        """\
        #if defined(__BYTE_ORDER__) && (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
            return bswap_\\1(p[i]);
        #else
            return p[i];
        #endif
        """
    )

    subcode = re.sub(
        r"getblock(.*?)(\s\(.*?\{\n).*?\}",
        "getblock\\1\\2" + BYTE_SWAP_IF_BIG_ENDIAN + "}",
        subcode,
        flags=re.DOTALL | re.MULTILINE,
    )

    return subcode


def transform_finalization_mixes(subcode: str) -> str:
    """Revise the finalization operations in MurmurHash3.

    Args:
        subcode (str): The code to be transformed.

    Returns:
        str: The transformed code.
    """

    transformations = [
        ["FORCE_INLINE", "static FORCE_INLINE"],
        ["int i", "Py_ssize_t i"],
    ]

    for tr in transformations:
        subcode = subcode.replace(tr[0], tr[1])

    return subcode


def expand_win_stdint_typedefs(subcode: str) -> str:
    """Delineate int type defitions for the older versions of the VS compiler.

    Args:
        subcode (str): The code to be transformed.

    Returns:
        str: The transformed code.
    """

    MSC_STDINT_TYPEDEFS = textwrap.dedent(
        """\
        typedef signed __int8 int8_t;
        typedef signed __int32 int32_t;
        typedef signed __int64 int64_t;
        typedef unsigned __int8 uint8_t;
        typedef unsigned __int32 uint32_t;
        typedef unsigned __int64 uint64_t;
        """
    )

    return re.sub(
        r"typedef unsigned char(.*)uint64_t;",
        MSC_STDINT_TYPEDEFS,
        subcode,
        flags=re.DOTALL,
    )


def append_mur_macros(subcode: str) -> str:
    """Append building blocks for multiply and rotate (MUR) operations.

    These functions are used by mmh3 hashers.

    In future updates, they may be also used by one-shot hash functions,
    although performance tests must be employed before such refactoring.

    Args:
        subcode (str): The code to be transformed.

    Returns:
        str: The transformed code.
    """
    subcode += "\n\n"

    subcode += textwrap.dedent(
        """\
        //-----------------------------------------------------------------------------
        // Building blocks for multiply and rotate (MUR) operations.
        // Names are taken from Google Guava's implementation
        """
    )

    subcode += "\n"

    subcode += textwrap.dedent(
        """\
        static FORCE_INLINE uint32_t
        mixK1(uint32_t k1)
        {
            const uint32_t c1 = 0xcc9e2d51;
            const uint32_t c2 = 0x1b873593;

            k1 *= c1;
            k1 = ROTL32(k1, 15);
            k1 *= c2;

            return k1;
        }
        """
    )

    subcode += textwrap.dedent(
        """\
        static FORCE_INLINE uint32_t
        mixH1(uint32_t h1, const uint32_t h2, const uint8_t shift, const uint32_t c1)
        {
            h1 = ROTL32(h1, shift);
            h1 += h2;
            h1 = h1 * 5 + c1;

            return h1;
        }
        """
    )

    subcode += textwrap.dedent(
        """\
        static FORCE_INLINE uint64_t
        mixK_x64_128(uint64_t k1, const uint8_t shift,
                    const uint64_t c1, const uint64_t c2)
        {
            k1 *= c1;
            k1 = ROTL64(k1, shift);
            k1 *= c2;

            return k1;
        }
        """
    )

    subcode += textwrap.dedent(
        """\
        static FORCE_INLINE uint64_t
        mixK1_x64_128(uint64_t k1)
        {
            const uint64_t c1 = BIG_CONSTANT(0x87c37b91114253d5);
            const uint64_t c2 = BIG_CONSTANT(0x4cf5ad432745937f);

            k1 *= c1;
            k1 = ROTL64(k1, 31);
            k1 *= c2;

            return k1;
        }
        """
    )

    subcode += textwrap.dedent(
        """\
        static FORCE_INLINE uint64_t
        mixK2_x64_128(uint64_t k2)
        {
            const uint64_t c1 = BIG_CONSTANT(0x87c37b91114253d5);
            const uint64_t c2 = BIG_CONSTANT(0x4cf5ad432745937f);

            k2 *= c2;
            k2 = ROTL64(k2, 33);
            k2 *= c1;

            return k2;
        }
        """
    )

    subcode += textwrap.dedent(
        """\
        static FORCE_INLINE uint64_t
        mixH_x64_128(uint64_t h1, uint64_t h2, const uint8_t shift, const uint32_t c)
        {
            h1 = ROTL64(h1, shift);
            h1 += h2;
            h1 = h1 * 5 + c;

            return h1;
        }
        """
    )

    subcode += textwrap.dedent(
        """\
        static FORCE_INLINE uint64_t
        mixK_x86_128(uint32_t k, const uint8_t shift, const uint32_t c1,
                    const uint32_t c2)
        {
            k *= c1;
            k = ROTL32(k, shift);
            k *= c2;

            return k;
        }
        """
    )

    return subcode


def generate_hasher_digest_x86_128_pre(subcode: str) -> str:
    """Generate the first part of the digest function for x86_128.

    Args:
        subcode (str): The constants in mmh3_x86_128.

    Returns:
        str: The first part of the digest function for x86_128.
    """
    hasher_digests = "\n\n"

    hasher_digests += textwrap.dedent(
        """\
        static FORCE_INLINE void
        digest_x86_128_impl(uint32_t h1, uint32_t h2, uint32_t h3, uint32_t h4,
            const uint32_t k1, const uint32_t k2, const uint32_t k3,
            const uint32_t k4, const Py_ssize_t len, const char *out)
        {
        """
    )

    hasher_digests += subcode + "\n"

    return hasher_digests


def generate_hasher_digest_x86_128_main(subcode: str) -> str:
    """Generate the main part of the digest function for x86_128.

    Args:
        subcode (str): The finalization code in mmh3 x86_128.

    Returns:
        str: The main part of the digest function for x86_128.
    """
    hasher_digests = ""

    hasher_digests += textwrap.dedent(
        """\
        h1 ^= mixK_x86_128(k1, 15, c1, c2);
        h2 ^= mixK_x86_128(k2, 16, c2, c3);
        h3 ^= mixK_x86_128(k3, 17, c3, c4);
        h4 ^= mixK_x86_128(k4, 18, c4, c1);
        """
    )

    hasher_digests += subcode + "\n"
    hasher_digests += textwrap.dedent(
        """\
        #if defined(__BYTE_ORDER__) && (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
            ((uint32_t *)out)[0] = bswap_32(h1);
            ((uint32_t *)out)[1] = bswap_32(h2);
            ((uint32_t *)out)[2] = bswap_32(h3);
            ((uint32_t *)out)[3] = bswap_32(h4);
        #else
            ((uint32_t *)out)[0] = h1;
            ((uint32_t *)out)[1] = h2;
            ((uint32_t *)out)[2] = h3;
            ((uint32_t *)out)[3] = h4;
        #endif
        """
    )
    hasher_digests += "\n}"

    return hasher_digests


def generate_hasher_digest_x64_128(subcode: str) -> str:
    """Generate the digest function for x64_128.

    Args:
        subcode (str): The finalization code in mmh3 x64_128.

    Returns:
        str: The digest function for x64_128.
    """
    hasher_digests = "\n\n"

    hasher_digests += textwrap.dedent(
        """\
        //-----------------------------------------------------------------------------
        // Finalization function
        """
    )

    hasher_digests += "\n"

    hasher_digests += textwrap.dedent(
        """\
        static FORCE_INLINE void
        digest_x64_128_impl(uint64_t h1, uint64_t h2, const uint64_t k1,
            const uint64_t k2, const Py_ssize_t len, const char *out)
        {
        """
    )
    hasher_digests += textwrap.dedent(
        """\
        h1 ^= mixK1_x64_128(k1);
        h2 ^= mixK2_x64_128(k2);
        """
    )
    hasher_digests += subcode + "\n"
    hasher_digests += textwrap.dedent(
        """\
        #if defined(__BYTE_ORDER__) && (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
            ((uint64_t *)out)[0] = bswap_64(h1);
            ((uint64_t *)out)[1] = bswap_64(h2);
        #else
            ((uint64_t *)out)[0] = h1;
            ((uint64_t *)out)[1] = h2;
        #endif
        """
    )
    hasher_digests += "\n}"

    return hasher_digests


def fix_non_win_force_inline(subcode: str) -> str:
    """Fix the FORCE_INLINE macro so that it works on old GCC and RHEL.

    Based on a commit from Micha Gorelick (@mynameisfiber).
    https://github.com/hajimes/mmh3/pull/1

    Args:
        subcode (str): The code to be transformed.

    Returns:
        str: The transformed code.
    """

    NON_WIN_FORCE_INLINE_ORIGINAL = (
        "#define	FORCE_INLINE inline __attribute__((always_inline))"
    )

    NON_WIN_FORCE_INLINE_REVISED = textwrap.dedent(
        """\
        #if ((__GNUC__ > 4) || (__GNUC__ == 4 && GNUC_MINOR >= 4))
        /* gcc version >= 4.4 4.1 = RHEL 5, 4.4 = RHEL 6. Don't inline for RHEL 5 gcc
        * which is 4.1*/
        #define FORCE_INLINE inline __attribute__((always_inline))
        #else
        #define FORCE_INLINE
        #endif
        """
    )

    return subcode.replace(NON_WIN_FORCE_INLINE_ORIGINAL, NON_WIN_FORCE_INLINE_REVISED)


def force_inline_force_inline(subcode: str) -> str:
    """Force inline to use static FORCE_INLINE.

    Args:
        subcode (str): The code to be transformed.

    Returns:
        str: The transformed code.
    """
    return re.sub(r"^inline ", "static FORCE_INLINE ", subcode, flags=re.MULTILINE)


def lowercase_function_names(subcode: str) -> str:
    """Lowercase functions names. Purely for style.

    Args:
        subcode (str): The code to be transformed.

    Returns:
        str: The transformed code.
    """

    function_names = [
        "MurmurHash3_x86_32",
        "MurmurHash3_x86_128",
        "MurmurHash3_x64_128",
    ]

    for fn in function_names:
        subcode = subcode.replace(fn, fn.lower())

    return subcode


if __name__ == "__main__":
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)

    original_source_path = os.path.join(dir_path, "smhasher/src/MurmurHash3.cpp")
    original_header_path = os.path.join(dir_path, "smhasher/src/MurmurHash3.h")

    new_source_name = "murmurhash3.c"
    new_header_name = "murmurhash3.h"
    file_header_name = "FILE_HEADER"

    new_source_path = os.path.join(dir_path, new_source_name)
    new_header_path = os.path.join(dir_path, new_header_name)
    file_header_path = os.path.join(dir_path, file_header_name)

    with open(original_source_path, "r") as source_file, open(
        original_header_path, "r"
    ) as header_file, open(file_header_path, "r") as file_header_file:
        source = MMH3Source(source_file.read())
        header = MMH3Header(header_file.read())
        file_header = file_header_file.read()

        new_source_builder = MMH3CodeBuilder()
        new_source_builder.add(file_header)
        new_source_builder.add(source.note_comment)
        new_source_builder.add(source.header_include, [str.lower])
        new_source_builder.add(
            source.body, [introduce_py_ssize_t, lowercase_function_names]
        )

        new_header_builder = MMH3CodeBuilder()
        new_header_builder.add(file_header)
        new_header_builder.add(
            header.header_guards_begin,
            [append_python_directives, append_byteswap_header],
        )
        new_header_builder.add(
            header.stdint,
            [expand_win_stdint_typedefs],
        )
        new_header_builder.add(
            source.macros,
            [fix_non_win_force_inline, force_inline_force_inline],
        )
        new_header_builder.add(
            source.getblock_functions,
            [transform_getblocks],
        )
        new_header_builder.add(
            "",
            [append_mur_macros],
        )
        new_header_builder.add(
            source.finalization_mixes,
            [transform_finalization_mixes],
        )
        new_header_builder.add(
            source.finalization_x64_128,
            [generate_hasher_digest_x64_128],
        )
        new_header_builder.add(
            source.constants_x86_128,
            [generate_hasher_digest_x86_128_pre],
        )
        new_header_builder.add(
            source.finalization_x86_128,
            [generate_hasher_digest_x86_128_main],
        )
        new_header_builder.add(
            header.declarations,
            [lowercase_function_names, introduce_py_ssize_t],
        )
        new_header_builder.add(header.header_guards_end)

        with open(new_source_path, "w") as f:
            f.write(new_source_builder.build())
        with open(new_header_path, "w") as f:
            f.write(new_header_builder.build())
