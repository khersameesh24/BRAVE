"""
Test module for AggregateUtils
"""

import unittest
from workflow.utils.utils_aggregate import AggregateUtils


class TestAggregateUtils(unittest.TestCase):
    """
    Test AggregateUtils used to run the aggregate
    snakefile with the BRAVE workflow
    """

    def setUp(self) -> None:
        self.out_dir: str = "test-out_dir"

    def test_generate_terminal_files(self):
        """
        Test if the terminal files are generated
        for the aggregate snakefile
        """
        terminal_files: list = AggregateUtils.generate_terminal_files(
            out_dir=self.out_dir,
        )

        assert (
            "test-out_dir/brave_analysis_aggregated_report.html"
            in terminal_files
        )
