from snakemake.utils import validate
from snakemake.logging import logger
from snakemake.utils import min_version
from utils.utils_pipeline import PipelineUtils


# set snakemake version
min_version("7.25.4")

# get the config/schema file loc
snakefile_loc: Path = Path(workflow.snakefile).parent
config_loc: Path = Path(snakefile_loc / "../config/brave_config.yaml").resolve()
logger.info(f"\nConfig : {config_loc}")

schema_loc: Path = Path(snakefile_loc / "../config/config.schema.yaml").resolve()
logger.info(f"Schema : {schema_loc}\n")


configfile: config_loc


# validate config with the config schema
validate(config, schema_loc)
logger.info("\nConfig validated")
# =================================================================================================
# get the qc module
stage_config = PipelineUtils.generate_step_config(config["pipeline"], config["stage"])


module stage:
    snakefile:
        "rules/stage.smk"
    config:
        stage_config


# run all rules from the declared modules
use rule * from stage as stage_*


# =================================================================================================
# orchestrate via rule all to generate output files from all modules
logger.info("\nExecuting brave stage workflow...")

onerror:
    """
    Executes only if the workflow fails with an error
    """
    logger.error("Data staging failed. Check logs for more details")

onsuccess:
    """
    Executes only if the workflow succeeds
    """
    logger.info("Data staged successfully.")

rule brave_stage:
    input:
        rules.stage_all.output,
    default_target: True
