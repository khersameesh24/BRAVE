import os
import unittest
from tempfile import TemporaryDirectory
from workflow.utils.utils_sample import SampleUtils


class TestSampleUtils(unittest.TestCase):
    """
    Test SampleUtils used to get sample info. to run the BRAVE workflow
    """

    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()

        # samplesheet - paired_end
        self.samplesheet_pe = os.path.join(
            self.temp_dir.name, "samplesheet_pe.csv"
        )

        with open(self.samplesheet_pe, "wt", encoding="utf-8") as sheet_pe:
            sheet_pe.write("sampleID,sampleType,fastq1,fastq2\n")
            sheet_pe.write(
                "HBR_Rep1,condition,HBR_Rep1_R1.fastq.gz,HBR_Rep1_R2.fastq.gz\n"
            )
            sheet_pe.write(
                "HBR_Rep2,condition,HBR_Rep2_R1.fastq.gz,HBR_Rep2_R2.fastq.gz\n"
            )
            sheet_pe.write(
                "HBR_Rep3,condition,HBR_Rep3_R1.fastq.gz,HBR_Rep3_R2.fastq.gz\n"
            )
            sheet_pe.write(
                "UHR_Rep1,control,UHR_Rep1_R1.fastq.gz,UHR_Rep1_R2.fastq.gz\n"
            )
            sheet_pe.write(
                "UHR_Rep2,control,UHR_Rep2_R1.fastq.gz,UHR_Rep2_R2.fastq.gz\n"
            )
            sheet_pe.write(
                "UHR_Rep3,control,UHR_Rep3_R1.fastq.gz,UHR_Rep3_R2.fastq.gz\n"
            )

        # samplesheet - single_end
        self.samplesheet_se = os.path.join(
            self.temp_dir.name, "samplesheet_se.csv"
        )

        with open(self.samplesheet_se, "wt", encoding="utf-8") as sheet_se:
            sheet_se.write("sampleID,sampleType,fastq\n")
            sheet_se.write("HBR_Rep1,condition,HBR_Rep1.fastq.gz\n")
            sheet_se.write("HBR_Rep2,condition,HBR_Rep2.fastq.gz\n")
            sheet_se.write("HBR_Rep3,condition,HBR_Rep3.fastq.gz\n")
            sheet_se.write("UHR_Rep1,control,UHR_Rep1.fastq.gz\n")
            sheet_se.write("UHR_Rep2,control,UHR_Rep2.fastq.gz\n")
            sheet_se.write("UHR_Rep3,control,UHR_Rep3.fastq.gz\n")

    def test_get_sample_info_pe(self):
        """
        Test if the samplesheet is read and returns sampleinfo
        for paired_end samples
        """
        sample_info: dict = SampleUtils.get_sample_info(
            samplesheet=self.samplesheet_pe, sample_type="paired_end"
        )
        expected_sample_info: dict = {
            "control": ["UHR_Rep1", "UHR_Rep2", "UHR_Rep3"],
            "condition": ["HBR_Rep1", "HBR_Rep2", "HBR_Rep3"],
            "sample_fastq": {
                "control": [
                    "UHR_Rep1_R1.fastq.gz",
                    "UHR_Rep1_R2.fastq.gz",
                    "UHR_Rep2_R1.fastq.gz",
                    "UHR_Rep2_R2.fastq.gz",
                    "UHR_Rep3_R1.fastq.gz",
                    "UHR_Rep3_R2.fastq.gz",
                ],
                "condition": [
                    "HBR_Rep1_R1.fastq.gz",
                    "HBR_Rep1_R2.fastq.gz",
                    "HBR_Rep2_R1.fastq.gz",
                    "HBR_Rep2_R2.fastq.gz",
                    "HBR_Rep3_R1.fastq.gz",
                    "HBR_Rep3_R2.fastq.gz",
                ],
            },
        }
        self.assertDictEqual(sample_info, expected_sample_info)

    def test_get_sample_info_se(self):
        """
        Test if the samplesheet is read and returns sampleinfo
        for single_end samples
        """
        sample_info: dict = SampleUtils.get_sample_info(
            samplesheet=self.samplesheet_se, sample_type="single_end"
        )
        expected_sample_info: dict = {
            "control": ["UHR_Rep1", "UHR_Rep2", "UHR_Rep3"],
            "condition": ["HBR_Rep1", "HBR_Rep2", "HBR_Rep3"],
            "sample_fastq": {
                "control": [
                    "UHR_Rep1.fastq.gz",
                    "UHR_Rep2.fastq.gz",
                    "UHR_Rep3.fastq.gz",
                ],
                "condition": [
                    "HBR_Rep1.fastq.gz",
                    "HBR_Rep2.fastq.gz",
                    "HBR_Rep3.fastq.gz",
                ],
            },
        }
        self.assertDictEqual(sample_info, expected_sample_info)

    def test_check_fastq_files_ctrl(self):
        """
        Test if the control sample fastqs are located in the input dir
        """
        with self.assertRaises(FileNotFoundError):
            SampleUtils.check_fastq_files(
                in_dir=self.temp_dir.name,
                samples={
                    "control": ["UHR_Rep1"],
                    "condition": ["HBR_Rep1"],
                    "sample_fastq": {
                        "control": [
                            "UHR_Rep1_R1.fastq.gz",
                        ],
                        "condition": [
                            "HBR_Rep1_R1.fastq.gz",
                        ],
                    },
                },
            )

    def test_check_fastq_files_cond(self):
        """
        Test if the condition sample fastqs are located in the input dir
        """
        with self.assertRaises(FileNotFoundError):
            SampleUtils.check_fastq_files(
                in_dir=self.temp_dir.name,
                samples={
                    "control": ["UHR_Rep1"],
                    "condition": ["HBR_Rep1"],
                    "sample_fastq": {
                        "control": [
                            "UHR_Rep1_R1.fastq.gz",
                        ],
                        "condition": [
                            "HBR_Rep1_R1.fastq.gz",
                        ],
                    },
                },
            )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
