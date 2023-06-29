#!/usr/bin/env python3


import sys
import argparse
from pathlib import Path
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats


class DiffExp:
    """
    Class for implementation of the DESeq2 method
    for bulk-RNA Seq data analysis
    """

    def __init__(
        self,
        counts_file: Path,
        num_control: int,
        num_condition: int,
        filename: Path,
        num_cpu: int,
    ):
        self.counts_file: Path = counts_file
        self.num_control: int = num_control
        self.num_condition: int = num_condition
        self.filename: Path = filename
        self.num_cpu = num_cpu
        self.counts_matrix: pd.DataFrame = self.generate_counts_matrix()
        self.metadata: pd.DataFrame = self.generate_metadata()
        self.dds: pd.DataFrame = self.perform_diffexp_analysis()
        self.results: pd.DataFrame = self.get_dds_stats()
        self.generate_diffexp_genelist()

    def generate_counts_matrix(self):
        """
        Read the counts csv and return a transposed pd dataframe
        """
        if Path(self.counts_file).exists():
            counts = pd.read_csv(self.counts_file, delimiter="\t")

            # set the ensembl geneids as the dataframe index
            counts = counts.set_index("Geneid")

            # remove column with zero read counts
            counts = counts[counts.sum(axis=1) > 0]
            print(counts.T)
            return counts.T
        else:
            raise FileNotFoundError(
                f"Counts file {self.counts_file} not found. Check if it exists"
            )

    def generate_metadata(self):
        """
        Generate metadata to run deseq2
        """
        experiment: list = []
        for _ in range(self.num_control):
            experiment.append("Control")
        for _ in range(self.num_condition):
            experiment.append("Knockout")
        metadata = pd.DataFrame(
            zip(self.counts_matrix.index, experiment),
            columns=["Sample", "Condition"],
        )
        print(experiment)
        metadata = metadata.set_index("Sample")
        print(metadata)

        return metadata

    def perform_diffexp_analysis(self):
        """
        Run deseq2 on the counts matrix
        """
        dds = DeseqDataSet(
            counts=self.counts_matrix,
            clinical=self.metadata,
            design_factors="Condition",
        )

        # run deseq2
        dds.deseq2()

        return dds

    def get_dds_stats(self):
        """
        Run statistical test for differential expression
        """
        stats = DeseqStats(
            self.dds,
            n_cpus=self.num_cpu,
            contrast=("Condition", "Knockout", "Control"),
        )
        stats.summary()
        results_df = stats.results_df

        return results_df

    def generate_diffexp_genelist(self):
        self.results.to_csv(self.filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--counts-file",
        help="Counts matrix file from featurecounts",
        required=True,
        type=str,
        metavar="FILE",
    )
    parser.add_argument(
        "--num-control",
        help="Number of control samples in the study",
        required=True,
        type=int,
        metavar="INT",
    )
    parser.add_argument(
        "--num-condition",
        help="Number of condition samples in the study",
        required=True,
        type=int,
        metavar="INT",
    )
    parser.add_argument(
        "--out-file",
        help="Output file with differential gene expression analysis",
        required=True,
        type=str,
        metavar="FILE",
    )
    parser.add_argument(
        "--cpus",
        help="Number of CPUs to run deseq2 with.",
        required=False,
        default=4,
        type=int,
        metavar="INT",
    )

    # parse args
    args = parser.parse_args()

    counts_file = args.counts_file
    num_control = args.num_control
    num_condition = args.num_condition
    filename = args.out_file
    num_cpus = args.cpus

    # run the deseq analysis
    DiffExp(
        counts_file=counts_file,
        num_control=num_control,
        num_condition=num_condition,
        filename=filename,
        num_cpu=num_cpus,
    )
