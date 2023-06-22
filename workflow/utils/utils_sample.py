import sys
import csv
from pathlib import Path


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
        sheet_data: list = []
        samples: dict = {"control": [], "condition": [], "fastq_files": []}
        if Path(samplesheet).exists():
            with open(samplesheet, "r", encoding="utf-8") as sheet:
                samples_sheet = csv.DictReader(sheet)
                for sample_info in samples_sheet:
                    sheet_data.append(sample_info)

        for sample_info in sheet_data:
            if sample_info["sampleType"] == "control":
                samples["control"].append(sample_info["sampleID"])
            elif sample_info["sampleType"] == "condition":
                samples["condition"].append(sample_info["sampleID"])

            samples["fastq_files"].extend(
                [sample_info["read1"], sample_info["read2"]]
            )

        return samples

    @staticmethod
    def check_fastq_files(in_dir: Path, sample_files: list):
        """
        Check if the fastq files states in the samplesheet
        are present on the input directory path
        """
        for fastq in sample_files:
            path = Path(f"{in_dir}/{fastq}")
            if not Path(path).exists():
                print(
                    f"Fastq file {fastq} in samplesheet not found on the {in_dir}"
                )
                sys.exit(1)
