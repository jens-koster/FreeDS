import os

from freeds.config.file.config_classes import freeds_root, get_current_config_set


def get_env() -> dict[str, str]:
    """Get all envs asa dict.
    Root path and config url are always envs.
    Additionally any string value in the locals folder is converted to a env value, which should provide all secrets."""

    envs = {"FREEDS_ROOT_PATH": str(freeds_root()), "FREEDS_CONFIG_URL": "http://freeds-config:8005/api/configs/"}
    cfg_set = get_current_config_set()
    for cfg_file in cfg_set.locals.values():
        for key, value in cfg_file.get_config().items():
            if isinstance(value, str):
                env_name = f"FREEDS_{cfg_file.config_name.upper()}_{key.upper()}"
                envs[env_name] = value
    return envs


def set_env() -> None:
    """set all env values"""
    for key, value in get_env().items():
        os.environ[key] = value


def get_envs_as_export() -> list[str]:
    return [f'export {key}="{value}"' for key, value in get_env().items()]
