# colortimelog: A util for logging the time elapsed for a task.

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