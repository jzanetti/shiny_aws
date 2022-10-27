"""
Usage: app_utils --job showip/terminate --name bsis_shiny_example

Author: Sijin Zhang

Description: 
    This is a wrapper to obtain some basic information for an application, and update it if necessary

Debug:
    export PYTHONPATH=/home/szhang/Github/shiny_aws:$PYTHONPATH
"""

import argparse

from infras.apputils import UTILS_JOBS
from infras.apputils.aws import run_utils


def get_example_usage():
    example_text = """example:
        * app_utils --job showip/terminate/makeami/check --name bsis_shiny_example
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Shiny application utils (showip, check, terminate, or make an AMI)",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--job",
        required=True,
        choices=UTILS_JOBS,
        help="which job to be performed (showip, check, terminate or makeami)")

    parser.add_argument(
        "--name",
        required=True,
        help="the application name to be used")

    return parser.parse_args(
        # ["--job", "check", "--name", "bsis_mot_fleet"]
    )


def main(job: str, name: str):
    run_utils(job, name)

def app_utils_func():
    args = setup_parser()
    main(args.job, args.name)

if __name__ == "__main__":
    app_utils_func()

