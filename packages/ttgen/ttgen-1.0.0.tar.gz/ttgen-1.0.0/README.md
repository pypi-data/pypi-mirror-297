# TTGen

Efficient algorithm for generating all unique k-combinations of a set with duplicates, based on the algorithm by Tadao Takaoka [(2015, O(1) Time Generation of Adjacent Multiset Combinations)](https://arxiv.org/abs/1503.00067).

This is a pure Python implementation of the Pascal code provided by Tadao Takaoka in the linked article.

## Installation

Via ``pip``
```
pip install ttgen
```

Locally for development via
```
pip install -e .
```

## Publishing

Remember to increment the version number in ``pyproject.toml`` first.

```
python -m build
python -m twine upload dist/ttgen-X.Y.Z*
```

## Maintenance

- ``pytest`` to run unit tests