"""
Test module for DiffExp
"""

import unittest
from workflow.utils.utils_diffexp import DiffExpUtils


class TestDiffExpUtils(unittest.TestCase):
    """
    Test DiffExpUtils used to run the diffexp
    snakefile with the BRAVE workflow
    """

    def setUp(self) -> None:
        self.out_dir: str = "test-out_dir"

    def test_generate_terminal_files(self):
        """
        Test if the terminal files are generated for the diffexp snakefile
        """
        terminal_files: list = DiffExpUtils.generate_terminal_files(
            out_dir=self.out_dir,
        )

        assert ("test-out_dir/Differential_geneexp_analysis.csv"
                in terminal_files
                )
