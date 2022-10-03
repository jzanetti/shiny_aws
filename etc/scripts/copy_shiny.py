from glob import glob
from os.path import basename
from pathlib import Path
from subprocess import Popen

"""
Usage: copy_shiny --src /tmp/bsis.yml --dest_dir /tmp

Author: Sijin Zhang

Description: 
    This is a script to copy a local shiny application to S3

Debug:
    export PYTHONPATH=/home/szhang/Github/shiny_aws:$PYTHONPATH
"""

import argparse


def get_example_usage():
    example_text = """example:
        * copy_shiny --src examples/hello_world_mot --dest_dir s3://mot-shiny-app/examples
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Copy a shiny application to S3",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--src",
        required=True,
        help="The path of a local shiny application")

    parser.add_argument(
        "--dest_dir",
        required=True,
        help="S3 directory where to hold the shiny application")

    return parser.parse_args(
        # ["--src", "/home/szhang/Gitlab/shiny_app/r/fleet", "--dest_dir", "s3://mot-shiny-app/r/fleet/"]
    )



def copy_shiny():
    args = setup_parser()
    shiny_app_local = args.src
    shiny_app_s3 = args.dest_dir.strip("/")

    cmd = f"aws s3 sync {shiny_app_local} {shiny_app_s3}"
    print(cmd)
    fid = Popen(cmd, shell=True)
    fid.communicate()

if __name__ == "__main__":
    copy_shiny()
