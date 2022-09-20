"""
Usage: start_bsis --cfg /tmp/bsis.yml --workdir /tmp

Author: Sijin Zhang

Description: 
    This is a wrapper to start the asic Shiny Infrastructure Suite (BSIS) with
    - An EC2 instance (from spot market or on-demand)
    - Shiny application
    - Optional: attaching an Elastic IP address
    - Optional: Authentication based on `nginx`

Debug:
    export PYTHONPATH=/home/szhang/Github/shiny_aws:$PYTHONPATH
"""

import argparse

from infras.bsis.aws import create_infras
from infras.bsis.utils import read_cfg


def get_example_usage():
    example_text = """example:
        * start_bsis --cfg /tmp/bsis.yml --workdir /tmp
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Start a BSIS infrastructure",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--workdir",
        required=True,
        help="working directory to save intermediate files")

    parser.add_argument(
        "--cfg",
        required=True,
        help="BSIS configuration file path")

    return parser.parse_args(
        # ["--cfg", "etc/cfg/bsis_mot.yml", "--workdir", "bsis_run"]
    )


def main(workdir: str, cfg: dict):
    create_infras(workdir, cfg)

def start_bsis():
    args = setup_parser()
    cfg = read_cfg(args.cfg)
    main(args.workdir, cfg)

if __name__ == "__main__":
    start_bsis()

