# get stdlib modules
from sys import exit
from pathlib import Path


# get local modules
from snakemake.logging import logger
from utils.utils_metrics import MetricsUtils
from utils.utils_pipeline import PipelineUtils

# get the snakemake working directory
work_dir: Path = Path(config["work_dir"])

# define data flow directories
input_dir: Path = Path(f'{work_dir}/{config["results"]}/{config["input_dir"]}')
output_dir: Path = Path(f'{work_dir}/{config["results"]}/{config["output_dir"]}')

# define log & benchmark directories
log_dir: Path = Path(f'{output_dir}/{config["log_dir"]}')
benchmarks_dir: Path = Path(f'{output_dir}/{config["benchmarks_dir"]}')

# generate flattened samples list
flattended_samples: list = []
flattended_samples.extend(config["samples_control"])
flattended_samples.extend(config["samples_condition"])

# get available resources
memory: float = PipelineUtils.get_available_memory()
cores: int = PipelineUtils.get_max_cores()


# generate a list of all files to be generated by rule `all` (terminal files)
terminal_files: list = MetricsUtils.generate_terminal_files(
    in_dir=input_dir,
    out_dir=output_dir,
    flattened_sample_list=flattended_samples,
    sample_type=config["sample_type"],
)

onerror:
    """
    Executes only if the workflow fails with an error
    """
    logger.error(
        f"Workflow failed at the metrics step. Check logs for more details"
    )
    exit(1)

onsuccess:
    """
    Executes only if the workflow succeeds
    """
    logger.error("Workflow executed successfully with no error")


rule all:
    """
    Generate all terminal files for the snakemake rule(s) below
    """
    input:
        terminal_files,
    output:
        temp(touch(f"{work_dir}/progress/metrics.done")),


rule run_samtools_build_index:
    """
    Runs samtools `index` and generates bam index that
    allows fast look-up of data in a BAM file
    """
    input:
        bam_in=input_dir / "{sample}_Aligned.sortedByCoord.out.bam",
    output:
        bam_bai=input_dir / "{sample}_Aligned.sortedByCoord.out.bai",
    conda:
        "../envs/env_metrics.yaml"
    priority: 1
    message:
        "Running samtools `index` for sample {wildcards.sample}"
    log:
        log_dir / "build_index" / "{sample}.build_index.log",
    benchmark:
        benchmarks_dir / "build_index" / "{sample}.build_index.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        samtools \
        index {input.bam_in} \
        {output.bam_bai} \
        -@ {threads} \
        &> {log}
        """


rule run_picard_markduplicates:
    """
    Runs picard `MarkDuplicates` to identify duplicate reads &
    locates and tags duplicate reads in a BAM or SAM file,
    where duplicate reads are defined as originating from a
    single fragment of DNA.
    """
    input:
        bam_in=input_dir / "{sample}_Aligned.sortedByCoord.out.bam",
    output:
        bam_out=output_dir
        / "markdup"
        / "{sample}_Aligned.sortedByCoord.out.markdup.bam",
        metrics_out=output_dir / "markdup" / "{sample}.MarkDuplicates.metrics.txt",
    conda:
        "../envs/env_metrics.yaml"
    message:
        "Running picard `MarkDuplicates` for sample {wildcards.sample}"
    log:
        log_dir / "markdup" / "{sample}.markduplicates.log",
    benchmark:
        benchmarks_dir / "markdup" / "{sample}.markduplicates.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        picard \
        MarkDuplicates \
        --INPUT {input.bam_in} \
        --OUTPUT {output.bam_out} \
        --METRICS_FILE {output.metrics_out} \
        &> {log}
        """


rule run_samtools_bam_stats:
    """
    Runs samtools `index` and generates bam index that
    allows fast look-up of data in a BAM file
    """
    input:
        bam_in=input_dir / "{sample}_Aligned.sortedByCoord.out.bam",
    output:
        bam_stats=output_dir
        / "stats"
        / "{sample}_Aligned.sortedByCoord.out.bam_stats.txt",
    conda:
        "../envs/env_metrics.yaml"
    message:
        "Running samtools `stats` for sample {wildcards.sample}"
    log:
        log_dir / "stats" / "{sample}.stats.log",
    benchmark:
        benchmarks_dir / "stats" / "{sample}.stats.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        samtools \
        stats {input.bam_in} \
        -@ {threads} \
        &> {output.bam_stats} \
        2> {log}
        """


rule run_picard_alignment_summary:
    """
    Runs picard `CollectAlignmentSummaryMetrics` and produces metrics
    detailing the quality of the read alignments as well as the proportion
    of the reads that passed machine signal-to-noise threshold quality filters.
    """
    input:
        bam_in=input_dir / "{sample}_Aligned.sortedByCoord.out.bam",
        ref_seq=work_dir / "chr22_transcripts.fa",
    output:
        alignment_metrics=output_dir
        / "alignment_summary_metrics"
        / "{sample}_alignment_summary_metrics.txt",
    conda:
        "../envs/env_metrics.yaml"
    message:
        "Running picard `CollectAlignmentSummaryMetrics` for sample {wildcards.sample}"
    log:
        log_dir / "alignment_summary_metrics" / "{sample}.alignment_summary_metrics.log",
    benchmark:
        benchmarks_dir / "alignment_summary_metrics" / "{sample}.alignment_summary_metrics.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        picard \
        CollectAlignmentSummaryMetrics \
        --REFERENCE_SEQUENCE {input.ref_seq} \
        --INPUT {input.bam_in} \
        --OUTPUT {output.alignment_metrics} \
        &> {log}
        """


rule run_picard_estimate_complexity:
    """
    Runs picard `EstimateLibraryComplexity` & generate quality metrics 
    for a sequencing library preparation.
    Library complexity refers to the number of unique DNA fragments
    present in a given library.
    """
    input:
        bam_in=input_dir / "{sample}_Aligned.sortedByCoord.out.bam",
    output:
        metrics_out=output_dir
        / "libcomplexity_metrics"
        / "{sample}.est_lib_complex_metrics.txt",
    conda:
        "../envs/env_metrics.yaml"
    message:
        "Running picard `EstimateLibraryComplexity` for sample {wildcards.sample}"
    log:
        log_dir / "libcomplexity_metrics" / "{sample}.libcomplexity.log",
    benchmark:
        benchmarks_dir / "libcomplexity_metrics" / "{sample}.libcomplexity.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        picard \
        EstimateLibraryComplexity \
        --INPUT {input.bam_in} \
        --OUTPUT {output.metrics_out} \
        &> {log}
        """


rule run_picard_gcbiasmetrics:
    """
    Runs picard `CollectGcBiasMetrics`,
    & collects information about the relative
    proportions of G and C nucleotides in a sample.
    """
    input:
        bam_in=input_dir / "{sample}_Aligned.sortedByCoord.out.bam",
        ref_seq=work_dir / "chr22_transcripts.fa",
    output:
        gcbias_metrics_txt=output_dir / "gcbias_metrics" / "{sample}_gcbias.metrics.txt",
        gcbias_metrics_pdf=output_dir / "gcbias_metrics" / "{sample}_gcbias.metrics.pdf",
        gcbias_metrics_summary=output_dir
        / "gcbias_metrics"
        / "{sample}_gcbias.metrics.summary.txt",
    conda:
        "../envs/env_metrics.yaml"
    message:
        "Running picard `CollectGcBiasMetrics` for sample {wildcards.sample}"
    log:
        log_dir / "gcbias_metrics" / "{sample}.gcbiasmetrics.log",
    benchmark:
        benchmarks_dir / "gcbias_metrics" / "{sample}.gcbiasmetrics.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        picard \
        CollectGcBiasMetrics \
        --INPUT {input.bam_in} \
        --REFERENCE_SEQUENCE {input.ref_seq} \
        --OUTPUT {output.gcbias_metrics_txt} \
        --CHART_OUTPUT {output.gcbias_metrics_pdf} \
        --SUMMARY_OUTPUT {output.gcbias_metrics_summary} \
        &> {log}
        """


rule run_picard_insertsizemetrics_pe:
    """
    Runs picard 'CollectInsertSizeMetrics' & generate
    metrics for validating library construction,
    the insert size distribution and read
    orientation of paired-end libraries
    """
    input:
        bam_in=input_dir / "{sample}_Aligned.sortedByCoord.out.bam",
    output:
        insert_size_metrics_txt=output_dir
        / "insert_size_metrics"
        / "{sample}.insert_size_metrics.txt",
        insert_size_metrics_histogram=output_dir
        / "insert_size_metrics"
        / "{sample}.insert_size_Histogram.pdf",
    params:
        min_pct=0.5,
    conda:
        "../envs/env_metrics.yaml"
    message:
        "Running picard `CollectInsertSizeMetrics` for sample {wildcards.sample}"
    log:
        log_dir / "insert_size_metrics" / "{sample}.insert_size_metrics.log",
    benchmark:
        benchmarks_dir / "insert_size_metrics" / "{sample}.insert_size_metrics.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        picard \
        CollectInsertSizeMetrics \
        --INPUT {input.bam_in} \
        --OUTPUT {output.insert_size_metrics_txt} \
        --Histogram_FILE {output.insert_size_metrics_histogram} \
        --MINIMUM_PCT {params.min_pct} \
        &> {log}
        """


rule run_picard_rnaseq_metrics:
    """
    Runs picard `CollectRnaSeqMetrics` and
    generates metrics describing the distribution
    of the bases within the transcripts.
    """
    input:
        bam_in=input_dir / "{sample}_Aligned.sortedByCoord.out.bam",
        ref_flat_txt=work_dir / "refFlat_chr22.txt",
        ribosomal_intervals=work_dir / "chr22_ribosomal.interval_list",
    output:
        rnaseq_metrics=output_dir / "rnaseq_metrics" / "{sample}.rna_metrics",
    params:
        strand_specificity="NONE",
    conda:
        "../envs/env_metrics.yaml"
    message:
        "Running picard `CollectRnaSeqMetrics` for sample {wildcards.sample}"
    log:
        log_dir / "rnaseq_metrics" / "{sample}.rnaseq_metrics.log",
    benchmark:
        benchmarks_dir / "rnaseq_metrics" / "{sample}.rnaseq_metrics.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        picard \
        CollectRnaSeqMetrics \
        --INPUT {input.bam_in} \
        --OUTPUT {output.rnaseq_metrics} \
        --REF_FLAT {input.ref_flat_txt} \
        --STRAND_SPECIFICITY {params.strand_specificity} \
        &> {log}
        """
