# Big-O Estimator

This Python package allows you to estimate the Big-O complexity of Python functions using AST (Abstract Syntax Tree) parsing.

## Installation

You can install the package using:

```bash
pip install .
```

Usage

```python
from big_o_estimator import get_big_o_of_function

def sample_function(n):
    for i in range(n):
        pass

print(get_big_o_of_function(sample_function))
```
