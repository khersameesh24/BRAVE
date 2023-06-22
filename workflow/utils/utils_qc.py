"""
Utility class to generate terminal files for the fastqc snakefile
"""

from pathlib import Path
from snakemake.io import expand


class QCUtils:
    """
    Class for fastqc step utility functions
    """

    @staticmethod
    def generate_terminal_files(
        out_dir: Path, flattened_sample_list: list, sample_type: str = "paired"
    ) -> list:
        """
        Generate terminal files as final output files for run_fastqc rule.
        Args:
            out_dir - output directory to generate qc reports at
            flattened_sample_list - list of combined control/condition samples
            sample_type - type of library (paired/unpaired) default - paired
        """
        terminal_files: list = []
        output_ext: list = ["fastqc.zip", "fastqc.html"]
        if sample_type == "paired":
            paired_end_reads: list = ["R1", "R2"]

            terminal_files = expand(
                "{out_dir}/{sample}_{read}_{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                read=paired_end_reads,
                ext=output_ext,
            )

        elif sample_type == "unpaired":
            terminal_files = expand(
                "{out_dir}/{sample}_{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext=output_ext,
            )

        return terminal_files
