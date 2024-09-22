# Python starter with Poetry

This is a ready to use starter for Python packages, clone it and make sure to update:

* pyproject.toml
* README.md

## Develop locally

Start a new virtual env
```shell
poetry shel
```

Install all dependencies (declared on pyproject.toml)
```shell
poetry install
```

Add new dependency
```shell
poetry add requests
```

## Build and publish

Build package
```shell
poetry build
```

Publish package
```shell
poetry publish
```

Authenticate to PyPI
```shell
poetry config pypi-token.pypi $PYPI_TOKEN
```


# Referencs

[Guide to Python module](https://docs.python.org/3/tutorial/modules.htmldir)
[Python packaging user guide](https://packaging.python.org/en/latest/)