# mmh3 contribbuting guide

Thank you for your interest in contributing to the `mmh3` project!

Read [README.md](README.md) to get an overview of the `mmh3` project,
and follow our [Code of Conduct](./CODE_OF_CONDUCT.md)
(ACM Code of Ethics and Professional Conduct).

## Issues

You can contribute to our project by
simply submitting a bug report or a feature suggestion
through the [issue tracker](https://github.com/hajimes/mmh3/issues).

Before submitting a new issue, it's a good idea to check
[known issues on README](https://github.com/hajimes/mmh3#known-issues).

## Maitaining and developing the project

### Project structure

As of 4.1.0, the layout of the project is as follows:

- `src/mmh3`
  - `mmh3module.c`: this file
- `util`
  - `refresh.py`

### Testing

Before submitting your changes, make sure to run the project's tests to ensure
that everything is working as expected.
At least you should run `pytest` and `mypy --strict tests`
from the project root directory.

#### (Optional) Testing on s390x

When you changed the source in a way which may cause endian issues,
(...)

### Pull request

Finally, [create a pull request](https://github.com/hajimes/mmh3/pulls).
