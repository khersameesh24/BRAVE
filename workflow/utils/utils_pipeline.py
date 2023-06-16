class PipelineUtils:

    @staticmethod
    def generate_step_config(pipeline_config: dict, step_config: dict):
        """
        Generate a config dictionary for the snakemake module
        Args:
        pipeline_config: `pipeline` from config.yaml
        step_config: `step` from config.yaml
        """

        if pipeline_config and step_config:
            return {**pipeline_config, **step_config}
