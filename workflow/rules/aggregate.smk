# get stdlib modules
from pathlib import Path

# get local modules
from utils.utils_aggregate import AggregateUtils
from utils.utils_pipeline import PipelineUtils

# define data flow directories
work_dir: Path = Path(config["work_dir"])
input_dir: Path = Path(f'{work_dir}/{config["results"]}/')
output_dir: Path = Path(f'{input_dir}/{config["output_dir"]}')

# define log & benchmark directories
log_dir: Path = Path(f'{output_dir}/{config["log_dir"]}')
benchmarks_dir: Path = Path(f'{output_dir}/{config["benchmarks_dir"]}')

# generate flattened samples list
flattended_samples: list = []
flattended_samples.extend(config["sample_groups"]["control"])
flattended_samples.extend(config["sample_groups"]["condition"])

# get the config file loc
snakefile_loc: Path = Path(workflow.snakefile).parent
aggregate_config: Path = Path(
    snakefile_loc / "../../config/aggregate_config.yaml"
).resolve()

# get available resources
memory: float = PipelineUtils.get_available_memory()
cores: int = PipelineUtils.get_max_cores()

# generate a list of all files to be generated by rule `all` (terminal files)
terminal_files: list = AggregateUtils.generate_terminal_files(
    out_dir=output_dir,
)


rule all:
    """
    Generate all terminal files for the snakemake rule(s) below
    """
    input:
        terminal_files,
    output:
        temp(touch(f"{work_dir}/progress/aggregate.done")),


rule run_multiqc:
    """
    Runs Multiqc - & aggregates results from bioinformatics
    analyses across many samples into a single report
    """
    input:
        trimmed_out=expand(
            "{result_dir}/trimmed/{sample}.{ext}",
            result_dir=input_dir,
            sample=flattended_samples,
            ext="json",
        ),
        mapped_out=expand(
            "{result_dir}/mapped/{sample}_{ext}",
            result_dir=input_dir,
            sample=flattended_samples,
            ext=["ReadsPerGene.out.tab", "Log.final.out"],
        ),
        aln_summary_metrics_out=expand(
            "{result_dir}/metrics/{metric_dir}/{sample}_{ext}",
            result_dir=input_dir,
            metric_dir="alignment_summary_metrics",
            sample=flattended_samples,
            ext="alignment_summary_metrics.txt",
        ),
        gcbias_metrics_out=expand(
            "{result_dir}/metrics/{metric_dir}/{sample}_{ext}",
            result_dir=input_dir,
            metric_dir="gcbias_metrics",
            sample=flattended_samples,
            ext="gcbias.metrics.summary.txt",
        ),
        insert_size_metrics_out=expand(
            "{result_dir}/metrics/{metric_dir}/{sample}.{ext}",
            result_dir=input_dir,
            metric_dir="insert_size_metrics",
            sample=flattended_samples,
            ext="insert_size_metrics.txt",
        ),
        markdup_out=expand(
            "{result_dir}/metrics/{metric_dir}/{sample}.{ext}",
            result_dir=input_dir,
            metric_dir="markdup",
            sample=flattended_samples,
            ext="MarkDuplicates.metrics.txt",
        ),
        rnaseq_metrics_out=expand(
            "{result_dir}/metrics/{metric_dir}/{sample}.{ext}",
            result_dir=input_dir,
            metric_dir="rnaseq_metrics",
            sample=flattended_samples,
            ext="rna_metrics",
        ),
        bam_stats_out=expand(
            "{result_dir}/metrics/{metric_dir}/{sample}_{ext}",
            result_dir=input_dir,
            metric_dir="stats",
            sample=flattended_samples,
            ext="Aligned.sortedByCoord.out.bam_stats.txt",
        ),
        counts_out=input_dir / "counts/counts.out.summary",
    output:
        aggregate_outdir=directory(f"{output_dir}"),
        html_report=output_dir / "brave_analysis_aggregated_report.html",
    params:
        config_file=aggregate_config,
        html_filename="brave_analysis_aggregated_report",
    conda:
        "../envs/env_aggregate.yaml"
    message:
        "Running MultiQC"
    log:
        log_dir / "aggregate.log",
    benchmark:
        benchmarks_dir / "aggregate.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        multiqc \
        --config {params.config_file} \
        --filename {output.html_report} \
        --outdir {output.aggregate_outdir} \
        {input} \
        -f \
        &> {log}
        """
