"""
Setup brave command line utility
"""

from setuptools import setup
from workflow.utils.utils_pipeline import PipelineUtils


__version__ = PipelineUtils.get_version_info()

setup(
    name="brave",
    description="BRAVE - Bulk RNAseq Analysis & Visualization Engine",
    version=__version__,
    scripts=["bin/brave"],
    author="Sameesh Kher",
    author_email="khersameesh24@gmail.com",
    maintainer="Sameesh Kher",
    maintainer_email="khersameesh24@gmail.com",
    packages=["workflow", "config", "resources", "workflow/utils", "modules"],
    python_requires=">=3.8",
)
