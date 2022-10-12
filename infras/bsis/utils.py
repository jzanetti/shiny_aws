from os.path import basename

from yaml import safe_load


def read_cfg(cfg_path: str):
    """Read configuration file

    Args:
        cfg_path (str): configuration file path
    """
    with open(cfg_path, "r") as fid:
        cfg = safe_load(fid)

    return cfg

def obtain_cfg_name(cfg_path: str) -> str:
    """Get the configuration name from its path

    Args:
        cfg_path (str): configuration path

    Returns:
        str: configuration name
    """
    return basename(cfg_path).replace(".yml", "")

