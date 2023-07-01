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
        self.in_dir: str = "test_indir"
        self.out_dir: str = "test_outdir"
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
        expected_file_paths: list = [
            "test_indir/HBR_Rep1_Aligned.sortedByCoord.out.bai",
            "test_outdir/stats/HBR_Rep1_Aligned.sortedByCoord.out.bam_stats.txt",
            "test_outdir/libcomplexity_metrics/HBR_Rep1.est_lib_complex_metrics.txt",
            "test_outdir/markdup/HBR_Rep1_Aligned.sortedByCoord.out.markdup.bam",
            "test_outdir/markdup/HBR_Rep1.MarkDuplicates.metrics.txt",
            "test_outdir/alignment_summary_metrics/HBR_Rep1_alignment_summary_metrics.txt",
            "test_outdir/gcbias_metrics/HBR_Rep1_gcbias.metrics.txt",
            "test_outdir/gcbias_metrics/HBR_Rep1_gcbias.metrics.pdf",
            "test_outdir/gcbias_metrics/HBR_Rep1_gcbias.metrics.summary.txt",
            "test_outdir/insert_size_metrics/HBR_Rep1.insert_size_metrics.txt",
            "test_outdir/insert_size_metrics/HBR_Rep1.insert_size_Histogram.pdf",
            "test_outdir/rnaseq_metrics/HBR_Rep1.rna_metrics",
        ]
        self.assertListEqual(terminal_files, expected_file_paths)
