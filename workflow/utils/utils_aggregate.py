"""
Utility class to generate terminal files for the aggregate snakefile
"""


from pathlib import Path
from snakemake.logging import logger


class AggregateUtils:
    """
    Class for multiqc step utility functions
    """

    @staticmethod
    def generate_terminal_files(out_dir: Path) -> list:
        """
        Generate terminal files as final output files for run_aggregate rule.
        Args:
            out_dir - output directory to generate report files
        """
        terminal_files: list = [
            Path(f"{out_dir}"),
            f"{out_dir}/brave_analysis_aggregated_report.html",
        ]

        if terminal_files:
            logger.info("Terminal files generated for aggregate.")
        else:
            logger.error(
                f"{__name__} Failed to generate terminal files for aggregate."
            )
        return terminal_files
