from argparse import _ArgumentGroup
from snakemake import snakemake
from snakemake.logging import logger
from workflow.utils.utils_pipeline import PipelineUtils


DESCRIPTION = "Analyse your RNASeq data with the BRAVE"


def parse_args(parser: _ArgumentGroup) -> _ArgumentGroup:
    """
    Parse command line args for the BRAVE `analysis` module
    """
    # get the required args to run the analysis module
    required_named = parser.add_argument_group("Required Arguments")
    required_named.add_argument(
        "-i",
        "--input-dir",
        help="Path to the fastq files to be used by BRAVE analysis module.",
        required=True,
        metavar="PATH",
    )
    required_named.add_argument(
        "-s",
        "--sample-sheet",
        help="Path to the sample-sheet.csv to be used to get sample info.",
        required=True,
        metavar="FILE",
    )

    # get the optional args to run the analysis module
    optional_named = parser.add_argument_group("Optional Arguments")
    optional_named.add_argument(
        "-o",
        "--output-dir",
        help="Path to the output directory. Workflow results are generated here.",
        metavar="PATH",
    )
    optional_named.add_argument(
        "-w",
        "--work-dir",
        help="Path to the working directory.",
        metavar="PATH",
    )
    optional_named.add_argument(
        "-@",
        "--threads",
        help="Total threads for the Brave pipeline run.",
        metavar="INT",
    )
    optional_named.add_argument(
        "--unpaired",
        help="Default - `paired`. Type of sequencing library preparation.",
        action="store_true",
        default=False,
    )
    optional_named.add_argument(
        "--dry-run",
        help="Dry run brave workflow.",
        action="store_true",
        default=False,
    )
    optional_named.add_argument(
        "--quiet",
        help="Reduce verbosity for the brave workflow.",
        action="store_true",
        default=False,
    )
    optional_named.add_argument(
        "--dag",
        help="Get d3 compatible json of the DAG",
        action="store_true",
        default=False,
    )

    return parser


def execute_workflow(args: _ArgumentGroup) -> None:
    """
    Execute the analysis workflow with the command line arguments
    """
    # generate the additional config to be passed to snakemake
    add_config: dict = PipelineUtils.generate_additional_config(args)

    dry_run = add_config["pipeline"]["dry_run"]
    quiet_run = add_config["pipeline"]["quiet"]
    get_dag = add_config["pipeline"]["dag"]

    # get the available resources
    available_memory: float = PipelineUtils.get_available_memory()
    max_cores: int = PipelineUtils.get_max_cores()

    logger.info("Executing brave workflow...")
    snakemake(
        snakefile="workflow/Snakefile",
        printshellcmds=True,
        printreason=True,
        nocolor=False,
        cores=max_cores,
        force_incomplete=True,
        resources={"mem_gb": available_memory},
        use_conda=True,
        config=add_config,
        quiet=quiet_run,
        dryrun=dry_run,
        printd3dag=get_dag,
    )

    return None
