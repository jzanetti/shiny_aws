"""
Usage: make_base --cloud_init /tmp/cloud-init.sh
                 --cloud_init /tmp/spot_spec.sh
                 --ami_name ami_test
                 [--expected_duration 30]
                 [--overwrite_ami]

Author: Sijin Zhang

Description: 
    This is a wrapper to make a base AMI for Shiny_AWS

Debug:
    export PYTHONPATH=/home/szhang/Github/shiny_aws:$PYTHONPATH
"""

import argparse

from infras.base.aws import check_ami, make_ami, shutdown_instance


def get_example_usage():
    example_text = """example:
        * make_base --cloud_init /tmp/cloud-init.sh
                    --spot_spec /tmp/spot_spec.sh
                    --ami_name ami_test
                    [--expected_duration 45]
                    [--overwrite_ami]
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Start a base image, and then make an AMI",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--cloud_init",
        required=True,
        help="cloud-init file path")

    parser.add_argument(
        "--spot_spec",
        required=True,
        help="spot_spec.json file path")

    parser.add_argument(
        "--ami_name",
        required=True,
        type=str,
        help="ami name to be used")

    parser.add_argument(
        "--expected_duration",
        required=True,
        default=45,
        type=str,
        help="expected duration for making AMI in minutes")

    parser.add_argument(
        "--overwrite_ami", 
        action="store_true", 
        help="overwrite AMI if exists")


    return parser.parse_args(
        # [
        #    "--cloud_init", "/home/szhang/Github/shiny_aws/etc/aws/cloud-init-test.sh", 
        #    "--spot_spec", "/home/szhang/Github/shiny_aws/etc/aws/spot_spec_mot.json",
        #    "--ami_name", "sijin_test_ami",
        #    "--expected_duration", "3",
        #    "--overwrite_ami"
        # ]
    )


def main(cloud_init: str, spot_spec: str, ami_name: str, expected_duration: str, overwrite_ami: bool):
    check_ami(ami_name, overwrite_ami)
    make_ami(cloud_init, spot_spec, ami_name)
    shutdown_instance(expected_duration)

def start_base():
    args = setup_parser()
    main(args.cloud_init, args.spot_spec, args.ami_name, args.expected_duration, args.overwrite_ami)

if __name__ == "__main__":
    start_base()

