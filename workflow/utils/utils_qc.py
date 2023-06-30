"""
Utility class to generate terminal files for the qc snakefile
"""

from pathlib import Path
from snakemake.io import expand


class QCUtils:
    """
    Class for qc step utility functions
    """

    @staticmethod
    def generate_terminal_files(
        out_dir: Path,
        flattened_sample_list: list,
        sample_type: str = "paired_end"
    ) -> list:
        """
        Generate terminal files as final output files for run_fastp rule.
        Args:
            out_dir - output directory to generate qc reports at
            flattened_sample_list - list of combined control/condition samples
            sample_type - type of library (paired_end/single_end) default-paired_end
        """
        terminal_files: list = []
        if sample_type == "paired_end":
            terminal_files = expand(
                "{out_dir}/{sample}_{read}.{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                read=["R1", "R2"],
                ext="trimmed.fastq.gz",
            )

        elif sample_type == "single_end":
            terminal_files = expand(
                "{out_dir}/{sample}.{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext="trimmed.fastq.gz",
            )

        terminal_files.extend(
            expand(
                "{out_dir}/{sample}.{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext=["html", "json"],
            )
        )

        return terminal_files
