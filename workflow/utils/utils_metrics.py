from pathlib import Path
from snakemake.io import expand


class MetricsUtils:
    """
    Class for fastqc step utility functions
    """

    @staticmethod
    def generate_terminal_files(in_dir: Path, out_dir: Path, flattened_sample_list: list) -> list:
        """
        Generate terminal files as final output files for picard rules.
        Args:
            out_dir - output directory to generate mardup bam.
            sample_groups - list of sample name
        """
        terminal_files: list = []

        # samtools index output
        terminal_files.extend(
            expand(
                "{in_dir}/{sample}_{ext}",
                in_dir=in_dir,
                sample=flattened_sample_list,
                ext="Aligned.sortedByCoord.out.bai",
            )
        )
        # samtools stats output
        terminal_files.extend(
            expand(
                "{out_dir}/stats/{sample}_{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext="Aligned.sortedByCoord.out.bam_stats.txt",
            )
        )
        # picard estimate lib complexity
        terminal_files.extend(
            expand(
                "{out_dir}/libcomplexity_metrics/{sample}.{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext="est_lib_complex_metrics.txt",
            )
        )
        # picard markduplicates
        terminal_files.extend(
            expand(
                "{out_dir}/markdup/{sample}{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext=[
                    "_Aligned.sortedByCoord.out.markdup.bam",
                    ".MarkDuplicates.metrics.txt",
                ],
            )
        )
        # picard alignment summary
        terminal_files.extend(
            expand(
                "{out_dir}/alignment_summary_metrics/{sample}_{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext="alignment_summary_metrics.txt",
            )
        )
        # picard gcbias
        terminal_files.extend(
            expand(
                "{out_dir}/gcbias_metrics/{sample}_{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext=[
                    "gcbias.metrics.txt",
                    "gcbias.metrics.pdf",
                    "gcbias.metrics.summary.txt",
                ],
            )
        )
        # picard insert size
        terminal_files.extend(
            expand(
                "{out_dir}/insert_size_metrics/{sample}.{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext=["insert_size_metrics.txt", "insert_size_Histogram.pdf"],
            )
        )
        # rnaseq metrics
        terminal_files.extend(
            expand(
                "{out_dir}/rnaseq_metrics/{sample}.{ext}",
                out_dir=out_dir,
                sample=flattened_sample_list,
                ext="rna_metrics",
            )
        )

        return terminal_files
