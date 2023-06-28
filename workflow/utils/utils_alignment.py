"""
Utility class to generate terminal files for the fastqc snakefile
"""


from pathlib import Path
from snakemake.io import expand


class AlignmentUtils:
    """
    Class for star step utility functions
    """

    @staticmethod
    def generate_terminal_files(out_dir: Path, flattened_sample_list: list) -> list:
        """
        Generate terminal files as final output files for run_trimgalore rule.
        Args:
            out_dir - output directory to generate bam files
            flattened_samples_list - list of combined control/condition samples
        """
        terminal_files: list = []
        output_ext: list = [
            "Aligned.sortedByCoord.out.bam",
            "ReadsPerGene.out.tab",
            "SJ.out.tab",
            "Log.out",
            "Log.final.out",
            "Log.progress.out",
        ]
        terminal_files = expand(
            "{out_dir}/{sample}_{ext}",
            out_dir=out_dir,
            sample=flattened_sample_list,
            ext=output_ext,
        )

        return terminal_files
