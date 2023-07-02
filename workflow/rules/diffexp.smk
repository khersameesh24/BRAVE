# get stdlib modules
from sys import exit
from pathlib import Path

# get local modules
from utils.utils_pipeline import PipelineUtils
from utils.utils_diffexp import DiffExpUtils

# define data flow directories
work_dir: Path = Path(config["work_dir"])
input_dir: Path = Path(f'{work_dir}/{config["results"]}/{config["input_dir"]}')
output_dir: Path = Path(f'{work_dir}/{config["results"]}/{config["output_dir"]}')

# define log & benchmark directories
log_dir: Path = Path(f'{output_dir}/{config["log_dir"]}')
benchmarks_dir: Path = Path(f'{output_dir}/{config["benchmarks_dir"]}')

# get num samples
num_control = len(config["samples_control"])
num_condition = len(config["samples_condition"])

# get available resources
memory: float = PipelineUtils.get_available_memory()
cores: int = PipelineUtils.get_max_cores()

# generate a list of all files to be generated by rule `all` (terminal files)
terminal_files: list = DiffExpUtils.generate_terminal_files(
    out_dir=output_dir,
)

onerror:
    """
    Executes only if the workflow fails with an error
    """
    logger.error(
        f"Workflow failed at the diffexp step. Check logs for more details"
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
        temp(touch(f"{work_dir}/progress/diffexp.done")),


rule run_diffexp:
    """
    Runs pyDESeq - python implementation of the DESeq2 method
    for bulk-RNA Seq data analysis
    """
    input:
        counts_in=input_dir / "final_counts.out",
    output:
        diffexp_out=output_dir / "Differential_geneexp_analysis.csv",
    params:
        num_ctrl=num_control,
        num_cond=num_condition,
        cpus=cores,
    priority: 1
    conda:
        "../envs/env_diffexp.yaml"
    message:
        "Running PyDESeq"
    log:
        log_dir / "diffexp.log",
    benchmark:
        benchmarks_dir / "diffexp.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        workflow/scripts/deseq2.py \
        --counts-file {input.counts_in} \
        --num-control {params.num_ctrl} \
        --num-condition {params.num_cond} \
        --out-file {output.diffexp_out} \
        --cpus {params.cpus} \
        &> {log}
        """
