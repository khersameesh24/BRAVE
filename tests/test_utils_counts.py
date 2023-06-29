"""
Test module for CountsUtils
"""

import unittest
from workflow.utils.utils_counts import CountsUtils


class TestCountsUtils(unittest.TestCase):
    """
    Test CountsUtils used to run the counts
    snakefile with the BRAVE workflow
    """

    def setUp(self) -> None:
        self.out_dir: str = "test-out_dir"

    def test_generate_terminal_files(self):
        """
        Test if the terminal files are generated
        for the counts snakefile
        """
        terminal_files: list = CountsUtils.generate_terminal_files(
            out_dir=self.out_dir,
        )

        assert "test-out_dir/counts.out" in terminal_files
        assert "test-out_dir/final_counts.out" in terminal_files
        assert "test-out_dir/counts.out.summary" in terminal_files
