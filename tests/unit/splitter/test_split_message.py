import unittest
from dataclasses import dataclass
from pathlib import Path

from src.exceptions.fragment_too_long import FragmentTooLongError
from src.splitter import split_message


@dataclass
class TestFileCasesTestCases:
    filename: str
    max_len: int
    result_fragments_len: list[int]


class TestSplitMessage(unittest.TestCase):
    def setUp(self):
        self.html_files_fir_path = Path.cwd() / "tests" / "html_files"

    def get_html_file_content(self, filename: str):
        file_path = self.html_files_fir_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Not found test html file {file_path}")

        with file_path.open("r") as f:
            return f.read()

    def test_basic(self, *args):
        result = list(split_message("<p>Hello, world!</p>", max_len=50))
        self.assertEqual(result, ["<p>Hello, world!</p>"])

        result = list(split_message("<p>Hello, world!</p>" * 3, max_len=20))
        self.assertEqual(result, ["<p>Hello, world!</p>"] * 3)

    def test_too_long_fragment(self):
        with self.assertRaises(FragmentTooLongError):
            list(split_message("<p>Hello, world!</p>", max_len=5))

    def test_files_cases(self):
        test_cases = [
            TestFileCasesTestCases(
                filename="test-1.html",
                max_len=4396,
                result_fragments_len=[
                    4370,
                    1370,
                ],
            ),
            TestFileCasesTestCases(
                filename="test-1.html",
                max_len=4296,
                result_fragments_len=[
                    4248,
                    1492,
                ],
            ),
            TestFileCasesTestCases(
                filename="test-2.html",
                max_len=4396,
                result_fragments_len=[
                    751,
                    4319,
                    660,
                ],
            ),
        ]

        for test_case in test_cases:
            content = self.get_html_file_content(test_case.filename)
            fragments = list(split_message(content, max_len=test_case.max_len))

            self.assertEqual(
                len(fragments), len(test_case.result_fragments_len)
            )
            for i, fragment in enumerate(fragments):
                self.assertEqual(
                    len(fragment), test_case.result_fragments_len[i]
                )


if __name__ == "__main__":
    unittest.main()
