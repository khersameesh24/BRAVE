"""
Utility class to generate terminal files for the aggregate snakefile
"""


from pathlib import Path


class AggregateUtils:
    """
    Class for multiqc step utility functions
    """

    @staticmethod
    def generate_terminal_files(out_dir: Path) -> list:
        """
        Generate terminal files as final output files for run_trimgalore rule.
        Args:
            out_dir - output directory to generate bam files
            flattened_samples_list - list of combined control/condition samples
        """
        terminal_files: list = [
            Path(f"{out_dir}"),
            f"{out_dir}/brave_analysis_aggregated_report.html",
        ]

        return terminal_files
