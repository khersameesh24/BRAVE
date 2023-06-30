"""
Test module for AggregateUtils
"""

import unittest
from pathlib import Path
from workflow.utils.utils_aggregate import AggregateUtils


class TestAggregateUtils(unittest.TestCase):
    """
    Test AggregateUtils used to run the aggregate
    snakefile with the BRAVE workflow
    """

    def setUp(self) -> None:
        self.out_dir: str = "test_outdir"

    def test_generate_terminal_files(self):
        """
        Test if the terminal files are generated
        for the aggregate snakefile
        """
        terminal_files: list = AggregateUtils.generate_terminal_files(
            out_dir=self.out_dir,
        )
        expected_file_paths: list = [
            Path("test_outdir"),
            "test_outdir/brave_analysis_aggregated_report.html"
        ]
        self.assertListEqual(
            terminal_files,
            expected_file_paths
        )
