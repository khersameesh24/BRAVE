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
        self.out_dir: str = "test_outdir"
        self.flattened_samples: list = ["HBR_Rep1", "HBR_Rep2"]

    def test_generate_terminal_files_pe(self) -> None:
        """
        Test if the terminal files are generated in case of
        paired-end samples
        """
        terminal_files: list = QCUtils.generate_terminal_files(
            out_dir=self.out_dir,
            flattened_sample_list=self.flattened_samples,
            sample_type="paired_end",
        )
        expected_file_paths: list = [
            "test_outdir/HBR_Rep1_R1.trimmed.fastq.gz",
            "test_outdir/HBR_Rep1_R2.trimmed.fastq.gz",
            "test_outdir/HBR_Rep2_R1.trimmed.fastq.gz",
            "test_outdir/HBR_Rep2_R2.trimmed.fastq.gz",
            "test_outdir/HBR_Rep1.html",
            "test_outdir/HBR_Rep1.json",
            "test_outdir/HBR_Rep2.html",
            "test_outdir/HBR_Rep2.json",
        ]
        self.assertListEqual(
            terminal_files,
            expected_file_paths,
            ("Check if the generate_terminal_files "
             "function has the desired output for paired_end sample type.")
        )

    def test_generate_terminal_files_se(self) -> None:
        """
        Test if the terminal files are generated in case of
        single-end samples
        """
        terminal_files: list = QCUtils.generate_terminal_files(
            out_dir=self.out_dir,
            flattened_sample_list=self.flattened_samples,
            sample_type="single_end",
        )
        expected_file_paths: list = [
            "test_outdir/HBR_Rep1.trimmed.fastq.gz",
            "test_outdir/HBR_Rep2.trimmed.fastq.gz",
            "test_outdir/HBR_Rep1.html",
            "test_outdir/HBR_Rep1.json",
            "test_outdir/HBR_Rep2.html",
            "test_outdir/HBR_Rep2.json",
        ]
        self.assertListEqual(
            terminal_files,
            expected_file_paths,
            ("Check if the generate_terminal_files "
             "function has the desired output for single_end sample type.")
        )
