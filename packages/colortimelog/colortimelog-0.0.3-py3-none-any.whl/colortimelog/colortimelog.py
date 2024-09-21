"""A util for logging the time elapsed for a task."""

import contextlib
import functools
import time


class BColors:
  """A class for color printing in the terminal."""

  HEADER = "\033[95m"
  OKBLUE = "\033[94m"
  OKCYAN = "\033[96m"
  OKGREEN = "\033[92m"
  WARNING = "\033[93m"
  FAIL = "\033[91m"
  ENDC = "\033[0m"
  BOLD = "\033[1m"
  UNDERLINE = "\033[4m"


class TimeLog:
  """A class for timing and color printing."""

  def __init__(self, message: str):
    self.start_time = time.time()
    self.message = message

    print(BColors.OKGREEN, "[Start]", BColors.ENDC, self.message)

  def close(self):
    time_elapsed = time.time() - self.start_time
    if time_elapsed < 1e-6:
      time_str = "{:.3f}".format(time_elapsed * 1e9) + " nanoseconds"
    elif time_elapsed < 1e-3:
      time_str = "{:.3f}".format(time_elapsed * 1e6) + " microseconds"
    elif time_elapsed < 1:
      time_str = "{:.3f}".format(time_elapsed * 1e3) + " milliseconds"
    elif time_elapsed > 3600:
      time_str = "{:.3f}".format(time_elapsed / 3600) + " hours"
    elif time_elapsed > 60:
      time_str = "{:.3f}".format(time_elapsed / 60) + " minutes"
    else:
      time_str = "{:.3f}".format(time_elapsed) + " seconds"

    print(
        BColors.OKGREEN,
        "[ End ]",
        BColors.ENDC,
        self.message,
        BColors.OKBLUE,
        "| Took",
        time_str,
        BColors.ENDC,
    )


@contextlib.contextmanager
def timeblock(name):
  """A context manager for timing a block of code."""
  tl = TimeLog(name)
  try:
    yield tl
  finally:
    tl.close()


def timefunc(func):
  """A decorator for timing a function."""

  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    with timeblock(func.__name__):
      return func(*args, **kwargs)

  return wrapper
