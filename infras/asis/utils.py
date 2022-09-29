from json import dump as json_dump
from json import load as json_load
from os import makedirs
from os.path import basename, exists, join
from shutil import copytree, rmtree


def copy_asg_suite(src_suite: str, workdir: str) -> str:
    """Copying the asg CDK suite to a working directory

    Args:
        src_suite (str): the path of ASG CDK suite
        workdir (str): working directory
    """
    if exists(workdir):
        rmtree(workdir)
    makedirs(workdir)

    suite_dir = join(workdir, basename(src_suite))
    copytree(src_suite, suite_dir)

    return suite_dir



def update_cdk_json(cdk_suite: str, uuid: str, domain: str, ami: str, region: str):
    """Update CDK json configuration

    Args:
        cdk_suite (str): cdk suite (copied from src_suite)
        uuid (str): asis unique ID
        domain (str): domain name
    """
    cdk_json_path = join(cdk_suite, "cdk.json")
    with open(cdk_json_path, "r") as fid:
        json_cfg = json_load(fid)

    json_cfg["context"]["common"]["uuid"] = uuid
    json_cfg["context"]["common"]["ami"] = ami
    json_cfg["context"]["common"]["region"] = region
    json_cfg["context"]["route53"][
        "hosted_domain"]["name"] = domain.replace("www.", "")
    json_cfg["context"]["route53"]["record"]["name"] = domain

    with open(cdk_json_path, 'w') as fid:
        json_dump(json_cfg, fid)
