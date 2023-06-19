class PipelineUtils:
    """
    Utility functions for the brave pipeline run
    """

    @staticmethod
    def generate_step_config(pipeline_config: dict, step_config: dict) -> dict:
        """
        Generate a config dictionary for the snakemake module
        Args:
        pipeline_config: `pipeline` from config.yaml
        step_config: `step` from config.yaml
        """

        if pipeline_config and step_config:
            return {**pipeline_config, **step_config}

    @staticmethod
    def get_available_memory() -> float:
        """
        Get the available free memory for a brave run
        """
        available_memory = 4
        return available_memory

    @staticmethod
    def get_max_cores() -> int:
        """
        Get the number of cores available for a brave run
        """
        available_cores = 4
        return available_cores
