import sys
from pathlib import Path
from snakemake.logging import logger
import pandas as pd


class SampleUtils:
    """
    Utility class to process samplesheet data
    """

    @staticmethod
    def validate_samplesheet(
        samplesheet: Path, sample_type: str = "paired_end"
    ) -> pd.DataFrame:
        """
        Get sample sheet data from the input samplesheet
        Args:
            samplesheet - path to the sample-sheet.csv
            samples_type - paired/single end lib prep.
        """
        if Path(samplesheet).is_file() and Path(samplesheet).suffix == ".csv":
            sample_df: pd.DataFrame = pd.read_csv(
                samplesheet, delimiter=",", dtype=str, index_col=False
            )
            df_columns = list(sample_df.columns)
            for col_name in df_columns:
                idx = sample_df[sample_df[col_name] == ""].index
                if idx.any():
                    logger.error(
                        "Empty value(s) in samplesheet. Check if all the columns in samplsheet have a value."
                    )
                    sys.exit(1)

            if sample_type == "paired_end":
                column_names: list = [
                    "sampleID",
                    "sampleType",
                    "fastq1",
                    "fastq2",
                ]
                if df_columns == column_names:
                    logger.debug(
                        f"Samplesheet validated for {sample_type} run."
                    )
                elif len(df_columns) == 3 and df_columns[2] == "fastq":
                    logger.error(
                        "Check if the proper samplesheet is provided. Use `--unpaired` for single_end runs."
                    )
                    sys.exit(1)
                else:
                    logger.error(
                        "Samplesheet could not be validated for {sample_type} run."
                    )
                    sys.exit(1)

            elif sample_type == "single_end":
                column_names: list = ["sampleID", "sampleType", "fastq"]
                if df_columns == column_names:
                    logger.debug(
                        f"Samplesheet validated for {sample_type} run."
                    )
                elif (
                    len(df_columns) == 4
                    and df_columns[2] == "fastq1"
                    and df_columns[3] == "fastq2"
                ):
                    logger.info("Check if the proper samplesheet is provided.")
                    sys.exit(1)

        else:
            logger.error("Check if the samplesheet exists.")
            sys.exit(1)

        return sample_df

    @staticmethod
    def get_samples(
        sample_df: pd.DataFrame, sample_type: str = "paired_end"
    ) -> dict:
        """
        Get samples from the samplesheet to be updated in
        workflow config
        Args:
        sample_df - a dataframe containing sample info
        sample_type - paired/single end lib prep.
        """
        samples: dict = {}
        control_samples = sample_df.loc[
            sample_df["sampleType"] == "control", "sampleID"
        ].values.tolist()
        samples.update({"control": control_samples})
        condition_samples = sample_df.loc[
            sample_df["sampleType"] == "condition", "sampleID"
        ].values.tolist()
        samples.update({"condition": condition_samples})

        if sample_type == "paired_end":
            control_fastq = (
                sample_df.loc[
                    sample_df["sampleType"] == "control", ["fastq1", "fastq2"]
                ]
                .values.flatten()
                .tolist()
            )
            samples.update({"control_fastq": control_fastq})

            condition_fastq = (
                sample_df.loc[
                    sample_df["sampleType"] == "condition",
                    ["fastq1", "fastq2"],
                ]
                .values.flatten()
                .tolist()
            )
            samples.update({"condition_fastq": condition_fastq})

        elif sample_type == "single_end":
            control_fastq = sample_df.loc[
                sample_df["sampleType"] == "control", "fastq"
            ].tolist()
            samples.update({"control_fastq": control_fastq})

            condition_fastq = sample_df.loc[
                sample_df["sampleType"] == "condition", "fastq"
            ].tolist()
            samples.update({"condition_fastq": condition_fastq})

        return samples

    @staticmethod
    def check_fastq_files(
        in_dir: Path,
        samples: dict,
    ) -> None:
        """
        Check if the fastq files states in the samplesheet
        are present on the input directory path
        Args:
        in_dir - input directory with fastq files
        samples - sample info from the samplesheet
        """
        files_not_found: list = []
        if (
            "control_fastq" in samples.keys()
            and "condition_fastq" in samples.keys()
        ):
            sample_files: list = []
            sample_files.extend(samples["control_fastq"])
            sample_files.extend(samples["condition_fastq"])
            for file in sample_files:
                filepath = f"{in_dir}/{file}"
                if not Path(filepath).exists():
                    files_not_found.append(file)

            if files_not_found:
                logger.error(f"\nThe following files were not found at {in_dir}")
                logger.error("\n".join(files_not_found))
                sys.exit(1)
