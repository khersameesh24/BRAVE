"""
Test module for QCUtils
"""

import unittest
from workflow.utils.utils_qc import QCUtils


class TestQCUtils(unittest.TestCase):
    """
    Test QCUtils used to run the qc snakefile with the BRAVE workflow
    """

    def setUp(self) -> None:
        self.out_dir: str = "test-out_dir"
        self.flattened_samples: list = ["HBR_Rep1", "HBR_Rep2"]

    def test_generate_terminal_files_pe(self):
        """
        Test if the terminal files are generated in case of
        paired-end samples
        """
        terminal_files: list = QCUtils.generate_terminal_files(
            out_dir=self.out_dir,
            flattened_sample_list=self.flattened_samples,
            sample_type="paired",
        )

        assert "test-out_dir/HBR_Rep1_R1.trimmed.fastq.gz" in terminal_files
        assert "test-out_dir/HBR_Rep1_R2.trimmed.fastq.gz" in terminal_files
        assert "test-out_dir/HBR_Rep2_R1.trimmed.fastq.gz" in terminal_files
        assert "test-out_dir/HBR_Rep2_R2.trimmed.fastq.gz" in terminal_files
        assert "test-out_dir/HBR_Rep1.html" in terminal_files
        assert "test-out_dir/HBR_Rep1.json" in terminal_files
        assert "test-out_dir/HBR_Rep2.html" in terminal_files
        assert "test-out_dir/HBR_Rep2.json" in terminal_files

    def test_generate_terminal_files_se(self):
        """
        Test if the terminal files are generated in case of
        single-end samples
        """
        terminal_files: list = QCUtils.generate_terminal_files(
            out_dir=self.out_dir,
            flattened_sample_list=self.flattened_samples,
            sample_type="unpaired",
        )

        assert "test-out_dir/HBR_Rep1.trimmed.fastq.gz" in terminal_files
        assert "test-out_dir/HBR_Rep1.html" in terminal_files
        assert "test-out_dir/HBR_Rep1.json" in terminal_files
        assert "test-out_dir/HBR_Rep2.trimmed.fastq.gz" in terminal_files
        assert "test-out_dir/HBR_Rep2.html" in terminal_files
        assert "test-out_dir/HBR_Rep2.json" in terminal_files
