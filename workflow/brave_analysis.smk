from snakemake.utils import validate
from snakemake.utils import min_version
from snakemake.logging import logger
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
qc_config = PipelineUtils.generate_step_config(config["pipeline"], config["qc"])


module qc:
    snakefile:
        "rules/qc.smk"
    config:
        qc_config


# =================================================================================================
# get the alignment module
alignment_config = PipelineUtils.generate_step_config(
    config["pipeline"], config["alignment"]
)


module alignment:
    snakefile:
        "rules/alignment.smk"
    config:
        alignment_config


# =================================================================================================
# get the metrics module
metrics_config = PipelineUtils.generate_step_config(
    config["pipeline"], config["metrics"]
)


module metrics:
    snakefile:
        "rules/metrics.smk"
    config:
        metrics_config


# =================================================================================================
# get the counts module
counts_config = PipelineUtils.generate_step_config(config["pipeline"], config["counts"])


module counts:
    snakefile:
        "rules/counts.smk"
    config:
        counts_config


# =================================================================================================
# get the aggregate module
aggregate_config = PipelineUtils.generate_step_config(
    config["pipeline"], config["aggregate"]
)


module aggregate:
    snakefile:
        "rules/aggregate.smk"
    config:
        aggregate_config


# =================================================================================================
# get the diffexp module
diffexp_config = PipelineUtils.generate_step_config(
    config["pipeline"], config["diffexp"]
)


module diffexp:
    snakefile:
        "rules/diffexp.smk"
    config:
        diffexp_config


# =================================================================================================
# run all rules from the declared modules
use rule * from qc as qc_*


use rule * from alignment as alignment_*


use rule * from metrics as metrics_*


use rule * from counts as counts_*


use rule * from aggregate as aggregate_*


use rule * from diffexp as diffexp_*


# =================================================================================================
# orchestrate via rule all to generate output files from all modules
logger.info("\nExecuting brave analysis workflow...")
onsuccess:
    """
    Executes only if the workflow succeeds
    """
    logger.error(
        "\nBrave analysis workflow executed successfully with no error."
    )
    # mail -s "Brave analysis complete." khersameesh24@gmail.com < snakemake.log

onerror:
    """
    Executes only if the brave workflow fails with an error
    """
    logger.error(
        "\nBrave analysis workflow failed. Check logs for more details."
    )


rule brave_analysis:
    input:
        rules.qc_all.input,
        rules.alignment_all.input,
        rules.metrics_all.input,
        rules.counts_all.input,
        rules.aggregate_all.input,
        rules.diffexp_all.input,
    default_target: True
