from pathlib import Path
from argparse import _ArgumentGroup
import multiprocessing as mp
import psutil as ps
from workflow.utils.utils_sample import SampleUtils


class PipelineUtils:
    """
    Utility functions for the brave pipeline run
    """

    @staticmethod
    def get_version_info() -> str:
        """
        Get the BRAVE version info
        """
        __version__ = "1.0.1"
        return __version__

    @staticmethod
    def get_available_memory() -> float:
        """
        Get the available free memory for a brave run
        """
        available_memory: float = abs(
            int(ps.virtual_memory().available / (1024 * 1024))
        )
        return available_memory

    @staticmethod
    def get_max_cores() -> int:
        """
        Get the number of cores available for a brave run
        """
        available_cores: int = int(abs(mp.cpu_count() * 0.75))
        return available_cores

    @staticmethod
    def generate_step_config(pipeline_config: dict, step_config: dict) -> dict:
        """
        Generate a config dictionary for the snakemake module
        Args:
        pipeline_config: `pipeline` from config.yaml
        step_config: `step` from config.yaml
        """
        return {**pipeline_config, **step_config}

    @staticmethod
    def generate_additional_config(args: _ArgumentGroup) -> dict:
        """
        Generate a config dict to be passed to the snakemake executor
        """
        config: dict = {"pipeline": {}, "config_file": ""}

        # check if the input path exists
        if Path(args.input_dir).exists():
            config["pipeline"]["pipeline_input"] = args.input_dir
        else:
            print("Check if the input directory path exists.")
            exit(1)

        if args.output_dir and Path(args.output_dir):
            config["pipeline"]["pipeline_output"] = args.output_dir

        # get the sample info from samplesheet
        if Path(args.sample_sheet).exists():
            samples = SampleUtils.get_sample_info(
                samplesheet=args.sample_sheet
            )
            # check if the fastq files exists on the input directory
            SampleUtils.check_fastq_files(
                args.input_dir, samples["fastq_files"]
            )
            config["pipeline"]["sample_groups"] = samples
        else:
            print("Check if the sample-sheet path exists.")
            exit(1)

        # set the workflow working directory
        if args.work_dir:
            if Path(args.work_dir).exists():
                config["pipeline"]["work_dir"] = args.work_dir
        else:
            config["pipeline"]["work_dir"] = args.input_dir

        if args.unpaired:
            config["pipeline"]["sample_type"] = "unpaired"

        return config
