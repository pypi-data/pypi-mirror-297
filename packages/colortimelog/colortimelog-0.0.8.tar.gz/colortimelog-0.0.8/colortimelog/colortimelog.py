"""A util for logging the time elapsed for a task."""

import contextlib
import dataclasses
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
    self.closed = False
    self.message = message

    print(BColors.OKGREEN, "[Start]", BColors.ENDC, self.message)

  def close(self):
    """Close the time log."""
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
    self.closed = True

  def __del__(self):
    if not self.closed:
      self.close()


@contextlib.contextmanager
def timeblock(name: str):
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


@dataclasses.dataclass
class Logger:
  """A logger class with verbosity control."""

  verbosity: int = 3

  def verbosity_prefix(self, level: int) -> str:
    """Create a prefix for a message based on its verbosity level."""
    if level == 0:
      return BColors.FAIL + "[FATAL]" + BColors.ENDC
    elif level == 1:
      return BColors.OKBLUE + "[ERROR]" + BColors.ENDC
    elif level ==  2:
      return BColors.WARNING + "[WARNING]" + BColors.ENDC
    elif level ==  3:
      return BColors.BOLD + "[INFO]" + BColors.ENDC
    else:
      return BColors.OKCYAN + "[DEBUG]" + BColors.ENDC

  def print(self, level: int, message: str) -> None:
    """Print a message if level is not higher than verbosity.

    Args:
      level: the level of this message, smaller value means more important
      message: the message to be printed

    Raises:
      RuntimeError: if level is 0
    """
    if level <= self.verbosity:
      if level == 0:
        raise RuntimeError(self.verbosity_prefix(level) + " " + message)
      else:
        print(self.verbosity_prefix(level), message)

  def fatal(self, message: str) -> None:
    """Print a fatal message."""
    self.print(0, message)

  def error(self, message: str) -> None:
    """Print an error message."""
    self.print(1, message)

  def warning(self, message: str) -> None:
    """Print a warning message."""
    self.print(2, message)

  def info(self, message: str) -> None:
    """Print an info message."""
    self.print(3, message)

  def debug(self, message: str) -> None:
    """Print a debug message."""
    self.print(4, message)
