# get stdlib modules
from pathlib import Path

# get local modules
from utils.utils_fastqc import FastQCUtils

# define data flow directories
work_dir: Path = Path(config["work_dir"])
input_dir: Path = Path(config["pipeline_input"])
output_dir: Path = Path(f'{input_dir}/{config["output_dir"]}')

# define log & benchmark directories
log_dir: Path = Path(f'{output_dir}/{config["log_dir"]}')
benchmarks_dir: Path = Path(f'{output_dir}/{config["benchmarks_dir"]}')


# generate fastq file groups which serve as rule input
fastq_file_groups: dict = FastQCUtils.generate_fastq_groups(input_dir)
flattended_fastq_files: list = []
for filelist in list(fastq_file_groups.values()):
    for file_path in filelist:
        flattended_fastq_files.append(file_path)


# generate a list of all files to be generated by the run_fastqc rule (terminal files)
terminal_files: list = FastQCUtils.generate_terminal_files(
    out_dir=output_dir,
    flattened_file_list=flattended_fastq_files,
    fastq_ext=config["fastq_ext"],
)


rule all:
    input:
        terminal_files,
    output:
        temp(touch(f"{work_dir}/progress/fastqc.done")),


rule run_fastqc:
    """
    Runs Fastqc - A high throughput sequence QC analysis tool
    """
    input:
        fastq_in=input_dir / "{sample}.fastq.gz",
    output:
        fastq_zip=output_dir / "{sample}_fastqc.zip",
        fastq_html=output_dir / "{sample}_fastqc.html",
    params:
        outdir=output_dir,
    conda:
        config["env"]
    log:
        log_dir / "{sample}_fastqc.log",
    benchmark:
        benchmarks_dir / "{sample}_fastqc.benchmark.txt"
    threads: int(config["threads"])
    resources:
        mem_gb=4,
    shell:
        """
        mkdir -p {params.outdir}

        fastqc {input.fastq_in} \
        -t {threads} \
        --outdir {params.outdir} \
        --quiet \
        2> {log}
        """
