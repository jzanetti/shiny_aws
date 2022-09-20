from yaml import safe_load


def read_cfg(cfg_path: str):
    """Read configuration file

    Args:
        cfg_path (str): configuration file path
    """
    with open(cfg_path, "r") as fid:
        cfg = safe_load(fid)

    return cfg
