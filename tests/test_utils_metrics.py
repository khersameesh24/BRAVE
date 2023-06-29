"""
Test module for MetricsUtils
"""

import unittest
from workflow.utils.utils_metrics import MetricsUtils


class TestMetricsUtils(unittest.TestCase):
    """
    Test MetricsUtils used to run the metrics
    snakefile with the BRAVE workflow
    """

    def setUp(self) -> None:
        self.in_dir: str = "test-in_dir"
        self.out_dir: str = "test-out_dir"
        self.flattened_samples: list = ["HBR_Rep1"]

    def test_generate_terminal_files(self):
        """
        Test if the terminal files are generated for the metrics snakefile
        """
        terminal_files: list = MetricsUtils.generate_terminal_files(
            in_dir=self.in_dir,
            out_dir=self.out_dir,
            flattened_sample_list=self.flattened_samples,
        )

        assert (
            "test-in_dir/HBR_Rep1_Aligned.sortedByCoord.out.bai"
            in terminal_files
        )
        assert (
            "test-out_dir/stats/HBR_Rep1_Aligned.sortedByCoord.out.bam_stats.txt"
            in terminal_files
        )
        assert (
            "test-out_dir/libcomplexity_metrics/HBR_Rep1.est_lib_complex_metrics.txt"
            in terminal_files
        )
        assert (
            "test-out_dir/markdup/HBR_Rep1.MarkDuplicates.metrics.txt"
            in terminal_files
        )
        assert (
            "test-out_dir/markdup/HBR_Rep1_Aligned.sortedByCoord.out.markdup.bam"
            in terminal_files
        )
        assert (
            "test-out_dir/alignment_summary_metrics/HBR_Rep1_alignment_summary_metrics.txt"
            in terminal_files
        )
        assert (
            "test-out_dir/gcbias_metrics/HBR_Rep1_gcbias.metrics.txt"
            in terminal_files
        )
        assert (
            "test-out_dir/gcbias_metrics/HBR_Rep1_gcbias.metrics.pdf"
            in terminal_files
        )
        assert (
            "test-out_dir/gcbias_metrics/HBR_Rep1_gcbias.metrics.summary.txt"
            in terminal_files
        )
        assert (
            "test-out_dir/insert_size_metrics/HBR_Rep1.insert_size_metrics.txt"
            in terminal_files
        )
        assert (
            "test-out_dir/insert_size_metrics/HBR_Rep1.insert_size_Histogram.pdf"
            in terminal_files
        )
        assert (
            "test-out_dir/rnaseq_metrics/HBR_Rep1.rna_metrics"
            in terminal_files
        )
