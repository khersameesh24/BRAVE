import csv
from pathlib import Path
import yaml


class SampleUtils:
    """
    Utility class to process samplesheet data
    """

    @staticmethod
    def get_sample_info(samplesheet: Path) -> dict:
        """
        Get sample sheet data from the input samplesheet
        Args:
            samplesheet - path to the sample-sheet.csv
        """
        samples = []
        if Path(samplesheet).exists():
            with open(samplesheet, "r", encoding="utf-8") as sheet:
                samples_sheet = csv.DictReader(sheet)
                for sample_info in samples_sheet:
                    samples.append(sample_info)

            return samples
        else:
            raise FileExistsError("Check if the samplesheet path")

    @staticmethod
    def update_config_samples(
        samplesheet: Path, config_path: Path, pipeline_input: Path = None
    ) -> None:
        """
        Update sample info in the brave config
        Args:
            samplesheet - path to the sample-sheet.csv
            config_path - path to the brave config file 
        """
        samples: list = SampleUtils.get_sample_info(samplesheet)
        config_dict: dict = {}
        if Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as config:
                config_dict = yaml.full_load(config)

                samples_control: list = [
                    sample["sampleID"]
                    for sample in samples
                    if sample["sampleType"] == "control"
                ]
                samples_condition: list = [
                    sample["sampleID"]
                    for sample in samples
                    if sample["sampleType"] == "condition"
                ]
                config_dict["pipeline"]["sample_groups"][
                    "control"
                ] = samples_control
                config_dict["pipeline"]["sample_groups"][
                    "condition"
                ] = samples_condition

            if pipeline_input:
                config_dict["pipeline"]["pipeline_input"] = pipeline_input

            with open(config_path, "w", encoding="utf-8") as config:
                yaml.dump(config_dict, config)
        else:
            raise FileExistsError("Check if the config file exists.")

        return None
