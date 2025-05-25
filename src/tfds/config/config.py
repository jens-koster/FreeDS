from tfds.config_api import get_config as get_config_from_api
from tfds.config_api import is_api_avaiable
from tfds.config_file import get_config as get_config_from_file


def get_config(config_name: str) -> dict[str, str]:
    """Get a config, from api server if available or from file if avaiable."""
    if not config_name:
        raise ValueError("A config_name must be provided.")

    if is_api_avaiable():
        return get_config_from_api(config_name)
    else:
        return get_config_from_file(config_name)
