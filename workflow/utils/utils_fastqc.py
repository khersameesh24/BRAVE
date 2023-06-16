from pathlib import Path
from collections import defaultdict
import os


class FastQCUtils:
    """
    Class for fastqc step utility functions
    """

    @staticmethod
    def generate_fastq_groups(in_dir: Path,
                              sample_type: str = "paired",
                              fastq_ext: str = ".fastq.gz") -> dict:
        """Group fastq files
        together to return a file group
        Args:
            in_dir - Input folder with fastq output
        """
        if os.path.exists(in_dir):
            files = sorted(os.listdir(in_dir))
            file_groups: dict = defaultdict(lambda: [])
            for file in files:
                if file.endswith(fastq_ext):
                    if sample_type == "paired":
                        sample_name = file.split("_")[-3]
                        sample_num = file.split("_")[-2]
                        _sample_strnd = file.split("_")[-1]
                        key = f"{sample_name}_{sample_num}"
                        file_groups[key].append(f"{in_dir}/{file}")
        else:
            raise FileNotFoundError

        return file_groups

    @staticmethod
    def generate_terminal_files(out_dir: Path,
                                flattened_file_list: list,
                                fastq_ext: str = ".fastq.gz") -> list:
        """
        Generate terminal files as final output files for run_fastqc rule.
        Args:
            out_dir - output directory to generate qc reports. This
            comes from the config file
            flattened_file_list - list of fastq files from the input directory
        """
        terminal_files = []
        for file_path in flattened_file_list:
            # generate filepath with the user defined output paths
            base_name = os.path.basename(file_path)
            file_path = os.path.join(os.sep, out_dir, base_name)

            # change the file extension similiar to fastqc output
            zip_file_path = file_path.replace(fastq_ext, "_fastqc.zip")
            terminal_files.append(zip_file_path)
            html_file_path = file_path.replace(fastq_ext, "_fastqc.html")
            terminal_files.append(html_file_path)

        return terminal_files
