import logging
import sys
from typing import Optional


def setup_logging(
    tfds_package_names: list[str] = ["freeds", "tfds", "tfds_cli"],
    current_module: Optional[str] = None,
    tfds_level: int = logging.INFO,
    global_level: int = logging.WARNING,
) -> None:
    root_logger = logging.getLogger()

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(fmt="[%(asctime)s] %(levelname)s %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    if not root_logger.handlers:
        root_logger.addHandler(handler)

    # other packages
    root_logger.setLevel(global_level)  # Third-party default: only warn and up

    # our packages
    pkg_lst = tfds_package_names.copy()
    if current_module:
        pkg_lst.append(current_module.split(".")[0])

    for pkg in pkg_lst:
        package_logger = logging.getLogger(pkg)
        package_logger.setLevel(tfds_level)
