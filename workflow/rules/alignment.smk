# get stdlib modules
from pathlib import Path

# get local modules
from utils.utils_alignment import AlignmentUtils
from utils.utils_pipeline import PipelineUtils


# get the snakemake working directory
work_dir: Path = Path(config["work_dir"])

# define data flow directories
input_dir: Path = Path(f'{work_dir}/{config["results"]}/{config["input_dir"]}')
output_dir: Path = Path(f'{work_dir}/{config["results"]}/{config["output_dir"]}')
ref_genome: Path = Path(f'{work_dir}/{config["ref_genome"]}')

# define log & benchmark directories
log_dir: Path = Path(f'{output_dir}/{config["log_dir"]}')
benchmarks_dir: Path = Path(f'{output_dir}/{config["benchmarks_dir"]}')

# generate flattened samples list
flattended_samples: list = []
flattended_samples.extend(config["sample_groups"]["control"])
flattended_samples.extend(config["sample_groups"]["condition"])

# get available resources
memory: float = PipelineUtils.get_available_memory()
cores: int = PipelineUtils.get_max_cores()

# generate a list of all files to be generated by rule `all` (terminal files)
terminal_files: list = AlignmentUtils.generate_terminal_files(
    out_dir=output_dir, flattened_sample_list=flattended_samples
)


rule all:
    """
    Generate all terminal files for the snakemake rule(s) below
    """
    input:
        terminal_files,
    output:
        temp(touch(f"{work_dir}/progress/alignment.done")),


rule run_star_generate_index:
    """
    Runs star `genomeGenerate` to generate a reference genome path
    """
    input:
        fasta=work_dir / "chr22_transcripts.fa",
        gtf=work_dir / "chr22_genes.gtf",
    output:
        ref_genome=directory(f"{ref_genome}"),
    params:
        nbases=10,
    priority: 1
    conda:
        "../envs/env_alignment.yaml"
    log:
        log_dir / "star_genomegenerate.log",
    message:
        "Running STAR Genome Generate"
    benchmark:
        benchmarks_dir / "star_genomegenerate.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        STAR \
        --runMode genomeGenerate \
        --genomeDir {output.ref_genome} \
        --genomeFastaFiles {input.fasta} \
        --sjdbGTFfile {input.gtf} \
        --genomeSAindexNbases {params.nbases} \
        --runThreadN {threads} \
        &> {log}
        """


rule run_star_alignment_pe:
    """
    Runs star `alignReads` and generates a sorted bam file to be used to
    get the counts matrix
    """
    input:
        fastq_R1=input_dir / "{sample}_R1.trimmed.fastq.gz",
        fastq_R2=input_dir / "{sample}_R2.trimmed.fastq.gz",
        gtf=work_dir / "chr22_genes.gtf",
        ref_genome=rules.run_star_generate_index.output.ref_genome,
    output:
        bam_sorted=output_dir / "{sample}_Aligned.sortedByCoord.out.bam",
        reads_per_gene=output_dir / "{sample}_ReadsPerGene.out.tab",
        splice_junc=output_dir / "{sample}_SJ.out.tab",
        log_final_out=output_dir / "{sample}_Log.final.out",
        log_out=temp(output_dir / "{sample}_Log.out"),
        progress_out=temp(output_dir / "{sample}_Log.progress.out"),
    params:
        out_dir=output_dir,
    conda:
        "../envs/env_alignment.yaml"
    message:
        "Running STAR Alignment for sample {wildcards.sample}"
    log:
        log_dir / "{sample}.alignment.log",
    benchmark:
        benchmarks_dir / "{sample}.alignment.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        STAR \
        --runMode alignReads \
        --genomeDir {input.ref_genome} \
        --readFilesIn {input.fastq_R1} {input.fastq_R2} \
        --outSAMtype BAM SortedByCoordinate \
        --readFilesCommand zcat \
        --runThreadN {threads} \
        --quantMode GeneCounts \
        --outFileNamePrefix {params.out_dir}/{wildcards.sample}_ \
        --sjdbGTFfile {input.gtf} \
        &> {log}
        """


rule run_star_alignment_se:
    """
    Runs star `alignReads` and generates a sorted bam file to be used to
    get the counts matrix
    """
    input:
        trimmed_fastq=input_dir / "{sample}.trimmed.fastq.gz",
        gtf=work_dir / "chr22_genes.gtf",
        ref_genome=rules.run_star_generate_index.output.ref_genome,
    output:
        bam_sorted=output_dir / "{sample}_Aligned.sortedByCoord.out.bam",
        reads_per_gene=output_dir / "{sample}_ReadsPerGene.out.tab",
        splice_junc=output_dir / "{sample}_SJ.out.tab",
        log_final_out=output_dir / "{sample}_Log.final.out",
        log_out=temp(output_dir / "{sample}_Log.out"),
        progress_out=temp(output_dir / "{sample}_Log.progress.out"),
    params:
        out_dir=output_dir,
    conda:
        "../envs/env_alignment.yaml"
    message:
        "Running STAR Alignment for sample {wildcards.sample}"
    log:
        log_dir / "{sample}.alignment.log",
    benchmark:
        benchmarks_dir / "{sample}.alignment.benchmark.txt"
    threads: cores * 2
    resources:
        mem_gb=memory,
    shell:
        """
        STAR \
        --runMode alignReads \
        --genomeDir {input.ref_genome} \
        --readFilesIn {input.trimmed_fastq} \
        --outSAMtype BAM SortedByCoordinate \
        --readFilesCommand zcat \
        --runThreadN {threads} \
        --quantMode GeneCounts \
        --outFileNamePrefix {params.out_dir}/{wildcards.sample}_ \
        --sjdbGTFfile {input.gtf} \
        &> {log}
        """
