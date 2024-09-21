import unittest
import colortimelog


class TestTimeLog(unittest.TestCase):
  """Tests for the TimeLog class."""

  def test_timeblock(self):
    """Test the timeblock context manager."""
    with colortimelog.timeblock("test block"):
      pass

  def test_timefunc(self):
    """Test the timefunc decorator."""
    @colortimelog.timefunc
    def my_function() -> str:
      return "done"

    result = my_function()
    self.assertEqual(result, "done")


class TestLogger(unittest.TestCase):
  """Tests for the Logger class."""

  def test_info(self):
    """Test the info method."""
    logger = colortimelog.Logger(verbosity=3)
    logger.info("test info")

  def test_fatal(self):
    """Test the fatal method."""
    logger = colortimelog.Logger(verbosity=0)
    with self.assertRaises(RuntimeError):
      logger.fatal("test fatal")


if __name__ == "__main__":
  unittest.main()
