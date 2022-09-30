"""
Usage: start_asis
            --workdir /tmp/asis
            --ami ami-xxxx
            --region us-west-2
            [--cdk infras/asis/shiny_asg]
            [--uuid test]

Author: Sijin Zhang

Description: 
    This is a wrapper to start the asic Shiny Infrastructure Suite (ASIS) using .CDK

Debug:
    export PYTHONPATH=/home/szhang/Github/shiny_aws:$PYTHONPATH

    with input arguments:
        return parser.parse_args(
            [
                "--workdir", "/tmp/asis", 
                "--cdk", "/home/szhang/Github/shiny_aws/infras/asis/shiny_asg", 
                "--ami", "ami-06618c31796bff2cb",
                "--region", "ap-southeast-2",
                "--uuid", "r-shiny-asg",
                "--zone", "(mot-dev.link, Z0778680205QCZAT4YE40)",
            ]
"""

import argparse
from os.path import basename, join
from subprocess import call

from infras.asis.utils import copy_asg_suite, update_cdk_json


def get_example_usage():
    example_text = """example:
        * start_asis
            --workdir /tmp/asis
            --ami ami-xxx
            --region us-west-2
            [--cdk infras/asis/shiny_asg]
            [--uuid test]
            [--zone "(xxx-yyy.link, Z12345xyz)"]
            [--create_zone]
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Start an ASIS infrastructure via CDK",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )


    parser.add_argument(
        "--workdir",
        required=True,
        help="working directory")

    parser.add_argument(
        "--ami",
        required=True,
        help="base image AMI ID")

    parser.add_argument(
        "--region",
        required=True,
        help="AWS region")

    parser.add_argument(
        "--cdk",
        required=False,
        default="infras/asis/shiny_asg",
        help="CDK directory")

    parser.add_argument(
        "--uuid",
        required=False,
        default="r-shiny-asg",
        help="suite ID, e.g., r-shiny-asg")

    parser.add_argument(
        "--zone",
        required=False,
        default=None,
        help="Zone name and ID to be used(e.g., '(xxx-yyy.link, Z12345abcde)'), if None, a new zone will be created")

    parser.add_argument(
        "--create_zone", 
        help="create a new zone",
        action="store_true")

    return parser.parse_args()

def start_asis():
    args = setup_parser()

    cdk_suite = copy_asg_suite(args.cdk, args.workdir)
    update_cdk_json(
        cdk_suite, 
        args.uuid, 
        args.ami, 
        args.region, 
        args.zone,
        args.create_zone)
    call(
        ['./asis_trigger.sh'], 
        cwd = join(args.workdir, basename(args.cdk)),
        shell=True)

    print("done")

if __name__ == "__main__":
    start_asis()

