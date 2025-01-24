import unittest

from click.testing import CliRunner

from split_msg import main


class TestSplitMsg(unittest.TestCase):
    def test_wrong_file(self):
        result = CliRunner().invoke(
            main, ["not_exists_file.html", "--max-len", 100]
        )
        self.assertTrue(isinstance(result.exception, FileNotFoundError))
