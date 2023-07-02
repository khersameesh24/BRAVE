"""
Utility class to generate terminal files for the fastqc snakefile
"""

from pathlib import Path
from snakemake.logging import logger


class DiffExpUtils:
    """
    Class for fastqc step utility functions
    """

    @staticmethod
    def generate_terminal_files(out_dir: Path) -> list:
        """
        Generate terminal files as final output files for run_diffexp rule.
        Args:
            out_dir - output directory to generate qc reports at
        """
        terminal_files: list = []
        terminal_files = [f"{out_dir}/Differential_geneexp_analysis.csv"]

        if terminal_files:
            logger.info("Terminal files generated for diffexp.")
        else:
            logger.error(
                f"{__name__}: Failed to generate terminal files for diffexp."
            )

        return terminal_files
