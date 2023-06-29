"""
Test module for AlignmentUtils
"""

import unittest
from workflow.utils.utils_alignment import AlignmentUtils


class TestAlignmentUtils(unittest.TestCase):
    """
    Test AlignmentUtils used to run the alignment
    snakefile with the BRAVE workflow
    """

    def setUp(self) -> None:
        self.out_dir: str = "test-out_dir"
        self.flattened_samples: list = ["HBR_Rep1"]

    def test_generate_terminal_files(self):
        """
        Test if the terminal files are generated for the alignment snakefile
        """
        terminal_files: list = AlignmentUtils.generate_terminal_files(
            out_dir=self.out_dir,
            flattened_sample_list=self.flattened_samples,
        )

        assert (
            "test-out_dir/HBR_Rep1_Aligned.sortedByCoord.out.bam"
            in terminal_files
        )
        assert "test-out_dir/HBR_Rep1_ReadsPerGene.out.tab" in terminal_files
        assert "test-out_dir/HBR_Rep1_SJ.out.tab" in terminal_files
        assert "test-out_dir/HBR_Rep1_Log.out" in terminal_files
        assert "test-out_dir/HBR_Rep1_Log.final.out" in terminal_files
        assert "test-out_dir/HBR_Rep1_Log.progress.out" in terminal_files
