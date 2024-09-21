import unittest
import colortimelog


class TestTimeLog(unittest.TestCase):
  """Tests for the TimeLog class."""

  def test_timeblock(self):
    """Test the timeblock context manager."""
    with colortimelog.timeblock("test"):
      pass

  def test_timefunc(self):
    """Test the timefunc decorator."""
    @colortimelog.timefunc
    def my_function() -> str:
      return "done"

    result = my_function()
    self.assertEqual(result, "done")


if __name__ == "__main__":
  unittest.main()
