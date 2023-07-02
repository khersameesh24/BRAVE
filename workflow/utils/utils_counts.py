"""
Utility class to generate terminal files for the counts snakefile
"""

from pathlib import Path
from snakemake.logging import logger


class CountsUtils:
    """
    Class for counts step utility functions
    """

    @staticmethod
    def generate_terminal_files(
        out_dir: Path,
    ) -> list:
        """
        Generate terminal files as final output files for run_fastqc rule.
        Args:
            out_dir - output directory to generate qc reports at
            flattened_sample_list - list of combined control/condition samples
            sample_type - type of library (paired/unpaired) default - paired
        """
        terminal_files: list = []

        terminal_files = [
            f"{out_dir}/counts.out",
            f"{out_dir}/final_counts.out",
            f"{out_dir}/counts.out.summary",
        ]

        if terminal_files:
            logger.info("Terminal files generated for counts.")
        else:
            logger.error(
                f"{__name__}: Failed to generate terminal files for counts."
            )

        return terminal_files
