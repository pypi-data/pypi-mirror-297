from setuptools import setup

name = "types-python-jenkins"
description = "Typing stubs for python-jenkins"
long_description = '''
## Typing stubs for python-jenkins

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`python-jenkins`](https://opendev.org/jjb/python-jenkins) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`python-jenkins`.

This version of `types-python-jenkins` aims to provide accurate annotations
for `python-jenkins==1.8.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/python-jenkins. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`bde71c575f33fddcb71bbe0550facbfd08b5a6ae`](https://github.com/python/typeshed/commit/bde71c575f33fddcb71bbe0550facbfd08b5a6ae) and was tested
with mypy 1.11.1, pyright 1.1.381, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="1.8.0.20240921",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-jenkins.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-requests'],
      packages=['jenkins-stubs'],
      package_data={'jenkins-stubs': ['__init__.pyi', 'plugins.pyi', 'version.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
