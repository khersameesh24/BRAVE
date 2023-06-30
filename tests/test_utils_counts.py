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
        self.out_dir: str = "test_outdir"

    def test_generate_terminal_files(self):
        """
        Test if the terminal files are generated
        for the counts snakefile
        """
        terminal_files: list = CountsUtils.generate_terminal_files(
            out_dir=self.out_dir,
        )
        expected_file_paths: list = [
            "test_outdir/counts.out",
            "test_outdir/final_counts.out",
            "test_outdir/counts.out.summary"
        ]
        self.assertListEqual(
            terminal_files,
            expected_file_paths
        )
