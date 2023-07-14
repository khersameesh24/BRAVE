"""
Utility class to generate terminal files for the stage snakefile
"""

from pathlib import Path
from snakemake.io import expand
from snakemake.logging import logger


class StageUtils:
    """
    Class for stage step utility functions
    """

    @staticmethod
    def generate_terminal_files(
        out_dir: Path,
        sra_acc_list: list,
        sample_type: str = "paired_end",
        ext: str = "fastq.gz"
    ) -> list:
        """
        Generate terminal files as final output files for run_fasterqdump rule.
        Args:
            out_dir - output directory to generate qc reports at
            flattened_sample_list - list of combined control/condition samples
            sample_type - type of library paired_end/single_end
            ext - extension for the fastq files
        """
        terminal_files: list = []
        if sample_type == "paired_end":
            terminal_files = expand(
                "{out_dir}/{srr_acc}/{srr_acc}_{read}.{ext}",
                out_dir=out_dir,
                srr_acc=sra_acc_list,
                read=["1", "2"],
                ext=ext,
            )

        elif sample_type == "single_end":
            terminal_files = expand(
                "{out_dir}/{srr_acc}/{srr_acc}.{ext}",
                out_dir=out_dir,
                srr_acc=sra_acc_list,
                ext=ext,
            )

        terminal_files.extend(
            expand(
                "{out_dir}/{srr_acc}/{srr_acc}.sra",
                out_dir=out_dir,
                srr_acc=sra_acc_list,
            )
        )

        if terminal_files:
            logger.info("Terminal files generated for stage.")
        else:
            logger.error(
                f"{__name__} Failed to generate terminal files for stage."
            )

        return terminal_files

    @staticmethod
    def get_sra_ids(sra_filepath) -> list:
        """
        Get SRR ids from srr accession list file
        Args:
            sra_filepath - file contating list of srr ids
        """
        sra_acc_ids: list = []
        with open(sra_filepath, "r", encoding="utf-8") as sra_list:
            for sra_id in sra_list:
                sra_id = sra_id.strip().strip("\n")
                if sra_id:
                    sra_acc_ids.append(sra_id)

        return sra_acc_ids
