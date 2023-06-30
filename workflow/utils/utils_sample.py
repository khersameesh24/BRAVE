import sys
from pathlib import Path
import pandas as pd


class SampleUtils:
    """
    Utility class to process samplesheet data
    """

    @staticmethod
    def get_sample_info(samplesheet: Path,
                        sample_type: str = "paired_end") -> dict:
        """
        Get sample sheet data from the input samplesheet
        Args:
            samplesheet - path to the sample-sheet.csv
        """
        samples: dict = {
            "control": [],
            "condition": [],
            "sample_fastq": {"control": [], "condition": []},
        }
        if Path(samplesheet).is_file() and Path(samplesheet).suffix == ".csv":
            sample_df = pd.read_csv(
                samplesheet,
                delimiter=",",
                dtype=str,
                index_col=False
            )
            for _, row in sample_df.iterrows():
                if sample_type == "paired_end":
                    if row["sampleType"] == "control":
                        samples["control"].append(row["sampleID"])
                        samples["sample_fastq"]["control"].extend(
                            [row["fastq1"], row["fastq2"]]
                        )
                    elif row["sampleType"] == "condition":
                        samples["condition"].append(row["sampleID"])
                        samples["sample_fastq"]["condition"].extend(
                            [row["fastq1"], row["fastq2"]]
                        )

                elif sample_type == "single_end":
                    if row["sampleType"] == "control":
                        samples["control"].append(row["sampleID"])
                        samples["sample_fastq"]["control"].append(
                            row["fastq"]
                        )
                    elif row["sampleType"] == "condition":
                        samples["condition"].append(row["sampleID"])
                        samples["sample_fastq"]["condition"].append(
                            row["fastq"]
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
