from snakemake import snakemake
from workflow.utils.utils_pipeline import PipelineUtils
from workflow.utils.utils_sample import SampleUtils

DESCRIPTION = "Analyse your RNASeq data with the BRAVE"


def parse_args(parser):
    """
    Parse command line args for the BRAVE `analysis` module
    """
    # get the required args to run the analysis module
    required_named = parser.add_argument_group("Required Arguments")
    required_named.add_argument(
        "-i",
        "--input-dir",
        help="Path to the fastq files to be used by BRAVE.",
        required=True,
    )
    required_named.add_argument(
        "-s",
        "--sample-sheet",
        help="Path to the sample-sheet.csv to be used to get sample info.",
        required=True,
    )

    # get the optional args to run the analysis module
    optional_named = parser.add_argument_group("Optional Arguments")
    optional_named.add_argument(
        "-o",
        "--output-dir",
        help="Path to the output directory. Workflow results are generated here.",
    )
    optional_named.add_argument(
        "-c", "--config-file", help="Path to the user-defined config file "
    )
    return parser


def execute_workflow(args):
    # update sample keys in config
    SampleUtils.update_config_samples(
        samplesheet=args.sample_sheet,
        config_path="/home/sameesh/Portfolio/BRAVE/config/brave_config.yaml",
        pipeline_input=args.input_dir,
    )

    snakemake(
        snakefile="workflow/Snakefile",
        printshellcmds=True,
        printreason=True,
        nocolor=False,
        cores=PipelineUtils.get_max_cores(),
        force_incomplete=True,
        resources={"mem_gb": PipelineUtils.get_available_memory()},
        use_conda=True,
    )
