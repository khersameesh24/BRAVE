"""
Utility class to generate terminal files for the trimgalore snakefile
"""

from pathlib import Path
from snakemake.io import expand


class TrimmingUtils:
    """
    Class for trim_galore step utility functions
    """

    @staticmethod
    def generate_terminal_files(
        out_dir: Path, flattened_sample_list: list, sample_type: str = "paired"
    ) -> list:
        """
        Generate terminal files as final output files for run_trimgalore rule.
        Args:
            out_dir - output directory to generate trimmed fastq files
            flattened_sample_list - list of combined control/condition samples
            sample_type - type of library (paired/unpaired) default - paired
        """
        terminal_files: list = []
        if sample_type == "paired":
            output_ext = [
                "R1_val_1.fq.gz",
                "R1.fastq.gz_trimming_report.txt",
                "R2_val_2.fq.gz",
                "R2.fastq.gz_trimming_report.txt",
            ]
            terminal_files = expand(
                "{out_dir}/{sample}_{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext=output_ext,
            )

        elif sample_type == "unpaired":
            output_ext = [
                "_trimmed.fq.gz",
                ".fastq.gz_trimming_report.txt",
            ]
            terminal_files = expand(
                "{out_dir}/{sample}{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext=output_ext,
            )

        return terminal_files
