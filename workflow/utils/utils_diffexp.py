"""
Utility class to generate terminal files for the fastqc snakefile
"""

from pathlib import Path


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

        return terminal_files
