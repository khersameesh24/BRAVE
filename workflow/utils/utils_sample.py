import sys
import csv
from pathlib import Path


class SampleUtils:
    """
    Utility class to process samplesheet data
    """

    @staticmethod
    def get_sample_info(samplesheet: Path,
                        sample_type: "paired-end") -> dict:
        """
        Get sample sheet data from the input samplesheet
        Args:
            samplesheet - path to the sample-sheet.csv
        """
        sheet_data: list = []
        samples: dict = {
            "control": [],
            "condition": [],
            "sample_fastq": {"control": [], "condition": []},
        }
        if Path(samplesheet).exists():
            with open(samplesheet, "r", encoding="utf-8") as sheet:
                samples_sheet = csv.DictReader(sheet)
                for sample_info in samples_sheet:
                    sheet_data.append(sample_info)

        if sample_type == "paired-end":
            for sample_info in sheet_data:
                if sample_info["sampleType"] == "control":
                    samples["control"].append(sample_info["sampleID"])
                    samples["sample_fastq"]["control"].extend(
                        [sample_info["fastq1"], sample_info["fastq2"]]
                    )
                elif sample_info["sampleType"] == "condition":
                    samples["condition"].append(sample_info["sampleID"])
                    samples["sample_fastq"]["condition"].extend(
                        [sample_info["fastq1"], sample_info["fastq2"]]
                    )
        elif sample_type == "single-end":
            for sample_info in sheet_data:
                if sample_info["sampleType"] == "control":
                    samples["control"].append(sample_info["sampleID"])
                    samples["sample_fastq"]["control"].extend(
                        [sample_info["fastq"]]
                    )
                elif sample_info["sampleType"] == "condition":
                    samples["condition"].append(sample_info["sampleID"])
                    samples["sample_fastq"]["condition"].extend(
                        [sample_info["fastq"]]
                    )

        return samples

    @staticmethod
    def check_fastq_files(in_dir: Path, samples: dict):
        """
        Check if the fastq files states in the samplesheet
        are present on the input directory path
        """
        for ctrl_fastq, cond_fastq in zip(
            samples["sample_fastq"]["control"],
            samples["sample_fastq"]["condition"],
        ):
            ctrl_path = Path(f"{in_dir}/{ctrl_fastq}")
            cond_path = Path(f"{in_dir}/{cond_fastq}")
            if not Path(ctrl_path).exists():
                print(
                    f"Fastq file {ctrl_fastq} in samplesheet not found on the {in_dir}"
                )
                sys.exit(1)
            if not Path(cond_path).exists():
                print(
                    f"Fastq file {cond_fastq} in samplesheet not found on the {in_dir}"
                )
                sys.exit(1)
