from setuptools import setup

name = "types-greenlet"
description = "Typing stubs for greenlet"
long_description = '''
## Typing stubs for greenlet

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`greenlet`](https://github.com/python-greenlet/greenlet) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`greenlet`.

This version of `types-greenlet` aims to provide accurate annotations
for `greenlet==3.1.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/greenlet. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`9f033bf439e064917e4b235b8a09b7530f182516`](https://github.com/python/typeshed/commit/9f033bf439e064917e4b235b8a09b7530f182516) and was tested
with mypy 1.11.1, pyright 1.1.381, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="3.1.0.20240924",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/greenlet.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['greenlet-stubs'],
      package_data={'greenlet-stubs': ['__init__.pyi', '_greenlet.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
