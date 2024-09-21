# colortimelog: A util for logging the time elapsed for a task.

[![Python package](https://github.com/wq2012/colortimelog/actions/workflows/python-package.yml/badge.svg)](https://github.com/wq2012/colortimelog/actions/workflows/python-package.yml)
[![PyPI Version](https://img.shields.io/pypi/v/colortimelog.svg)](https://pypi.python.org/pypi/colortimelog)
[![Python Versions](https://img.shields.io/pypi/pyversions/colortimelog.svg)](https://pypi.org/project/colortimelog)
[![Downloads](https://static.pepy.tech/badge/colortimelog)](https://www.pepy.tech/projects/colortimelog)

## Install

```
pip install colortimelog
```

## Usage

Add timing for a function:

```python
import colortimelog

@colortimelog.timefunc
def my_function():
  ...
```

Add timeing for a block of code:

```python
import colortimelog

with colortimelog.timeblock("Doing XYC"):
  do_x()
  do_y()
  do_z()
```
