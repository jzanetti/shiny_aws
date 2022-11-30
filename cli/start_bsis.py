"""
Usage: start_bsis --cfg /tmp/bsis.yml --workdir /tmp [--lifespan 120]

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

from infras.bsis import DEFAULT_LIFESPAN_MINS, UNLIMITED_LIFESPAN_FLAG
from infras.bsis.aws import create_infras
from infras.utils import obtain_cfg_name, read_cfg


def get_example_usage():
    example_text = """example:
        * start_bsis --cfg /tmp/bsis.yml --workdir /tmp [--lifespan 60]
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

    parser.add_argument(
        "--lifespan",
        required=False,
        type=str,
        default=DEFAULT_LIFESPAN_MINS,
        help="Server lifespan in minutes (default: DEFAULT_LIFESPAN_MINS). "
             "For production deployment, please set this "
             f"to UNLIMITED_LIFESPAN_FLAG ({UNLIMITED_LIFESPAN_FLAG})")

    return parser.parse_args(
        # [
        #     "--workdir", "/tmp/bsis",
        #     "--cfg", "/Users/zhans/Gitlab/shiny_aws/etc/cfg/bsis_mot_example.yml",
        # ]
    )


def main(workdir: str, cfg: dict, lifespan: str, cfg_name: str):
    create_infras(workdir, cfg, lifespan, cfg_name)

def start_bsis():
    args = setup_parser()
    main(args.workdir, read_cfg(args.cfg), args.lifespan, obtain_cfg_name(args.cfg))

if __name__ == "__main__":
    start_bsis()

