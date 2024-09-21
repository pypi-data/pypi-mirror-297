# TTGen

Efficient algorithm for generating all unique k-combinations of a set with duplicates, based on the algorithm by Tadao Takaoka [(2015, O(1) Time Generation of Adjacent Multiset Combinations)](https://arxiv.org/abs/1503.00067).

This is a pure Python implementation of the Pascal code provided by Tadao Takaoka in the linked article.

## Performance

This implementation provides incredible speed-up compared to the default itertools implementation when generating multiset combinations with many duplicated elements (up to 5000× speed-up in the best tested case).

For cases where all elements are distinct, the default itertools implementation is consistently faster.

![Graph of benchmarking data](benchmarking/benchmarks.png)

## Installation

Via ``pip``
```
pip install ttgen
```

Locally for development via
```
pip install -e .[dev]
```

## Publishing

Remember to increment the version number in ``pyproject.toml`` first.

```
python -m build
python -m twine upload dist/ttgen-X.Y.Z*
```

## Maintenance

- ``pytest`` to run unit tests