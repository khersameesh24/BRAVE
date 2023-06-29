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
    python_requires=">=3.9",
    install_requires=[
        "coverage==7.2.7",
        "appdirs==1.4.4",
        "attrs==23.1.0",
        "certifi==2023.5.7",
        "charset-normalizer==3.1.0",
        "ConfigArgParse==1.5.3",
        "connection-pool==0.0.3",
        "coverage==7.2.7",
        "Cython==0.29.35",
        "datrie==0.8.2",
        "docutils==0.20.1",
        "dpath==2.1.5",
        "fastjsonschema==2.17.0",
        "gitdb==4.0.10",
        "GitPython==3.1.31",
        "humanfriendly==10.0",
        "idna==3.4",
        "Jinja2==3.1.2",
        "jsonschema==4.17.3",
        "jupyter_core==5.3.0",
        "MarkupSafe==2.1.2",
        "nbformat==5.8.0",
        "plac==1.3.5",
        "platformdirs==3.5.1",
        "psutil==5.9.5",
        "PuLP==2.7.0",
        "Pygments==2.15.1",
        "pyrsistent==0.19.3",
        "PyYAML==6.0",
        "requests==2.30.0",
        "reretry==0.11.8",
        "smart-open==6.3.0",
        "smmap==5.0.0",
        "snakemake==7.25.4",
        "stopit==1.1.2",
        "tabulate==0.9.0",
        "throttler==1.2.2",
        "toposort==1.10",
        "traitlets==5.9.0",
        "urllib3==2.0.2",
        "wrapt==1.15.0",
        "yte==1.5.1",
    ],
)
