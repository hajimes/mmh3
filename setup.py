from setuptools import Extension, setup

mmh3module = Extension(
    "mmh3", sources=["./src/mmh3/mmh3module.c", "./src/mmh3/murmurhash3.c"]
)

setup(
    ext_modules=[mmh3module],
    package_data={"mmh3": ["./src/mmh3/py.typed", "./src/mmh3/**.pyi"]},
)
