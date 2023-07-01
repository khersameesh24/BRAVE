from pathlib import Path
import multiprocessing as mp
from argparse import _ArgumentGroup
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
        max_cores: int = int(abs(mp.cpu_count() * 0.75))
        return max_cores

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
        Overwrite snakemake config from config.yaml
        """
        pipeline: dict = {}

        # check if the input path exists
        if Path(args.input_dir).exists():
            pipeline.update({"pipeline_input": args.input_dir})
        else:
            raise FileNotFoundError(
                "Check if the input directory path exists."
            )

        # check if the output path exists
        if args.output_dir and Path(args.output_dir):
            pipeline.update({"pipeline_output": args.output_dir})

        # check if the sample type is paired/single end
        if args.unpaired:
            pipeline.update({"sample_type": "single_end"})
        else:
            pipeline.update({"sample_type": "paired_end"})

        # get the sample info from samplesheet
        if Path(args.sample_sheet).exists():
            samples = SampleUtils.get_sample_info(
                samplesheet=args.sample_sheet,
                sample_type=pipeline["sample_type"],
            )
            # check if the fastq files exists on the input directory
            SampleUtils.check_fastq_files(
                in_dir=args.input_dir, samples=samples
            )
            pipeline.update(
                {
                    "samples_condition": samples["condition"]
                }
            )
            pipeline.update(
                {
                    "samples_control": samples["control"]
                }
            )
            pipeline.update(
                {"sample_fastq": samples["sample_fastq"]}
            )
        else:
            raise FileNotFoundError("Check if the sample-sheet path exists.")

        # set the workflow working directory
        if args.work_dir and Path(args.work_dir).exists():
            pipeline.update({"work_dir": args.work_dir})
        else:
            pipeline.update({"work_dir": args.input_dir})

        # check for a dry run
        if args.dry_run:
            pipeline.update({"dry_run": True})

        # check for verbosity
        if args.quiet:
            pipeline.update({"quiet": True})

        return {"pipeline": pipeline}
