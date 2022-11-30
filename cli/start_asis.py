"""
Usage: start_asis
            --workdir /tmp/asis
            --cfg etc/asis.yml

Author: Sijin Zhang

Description: 
    This is a wrapper to start the asic Shiny Infrastructure Suite (ASIS) using .CDK

Debug:
    export PYTHONPATH=/home/szhang/Github/shiny_aws:$PYTHONPATH
"""

import argparse
from os.path import basename
from subprocess import call

from infras.asis.aws import (copy_asg_suite, update_cdk_json,
                             update_cloud_init, write_trigger)
from infras.utils import read_cfg


def get_example_usage():
    example_text = """example:
        * start_asis
            --workdir /tmp/asis
            --cfg etc/asis_mot.yml
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
        "--cfg",
        required=True,
        help="ASIS configuration file path")

    return parser.parse_args(
        [
             "--workdir", "/tmp/asis",
             "--cfg", "/Users/zhans/Github/shiny_aws/etc/cfg/asis.yml",
        ]
    )


def start_asis():
    args = setup_parser()

    cdk_suite = copy_asg_suite(args.workdir)

    trigger_path = write_trigger(cdk_suite)

    cfg = read_cfg(args.cfg)

    uuid = basename(args.cfg).replace(".yml", "").replace("_", "-")

    update_cloud_init(args.workdir, cdk_suite, cfg)

    update_cdk_json(cdk_suite, uuid, cfg)

    call(
        [f'./{basename(trigger_path)}'], 
        cwd = cdk_suite,
        shell=True)

    print("done")

if __name__ == "__main__":
    start_asis()

