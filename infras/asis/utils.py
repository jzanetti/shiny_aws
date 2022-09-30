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



def update_cdk_json(cdk_suite: str, uuid: str, ami: str, region: str, zone: str, create_zone: bool):
    """Update CDK json configuration

    Args:
        cdk_suite (str): cdk suite (copied from src_suite)
        uuid (str): asis unique ID
        domain (str): domain name
    """
    cdk_json_path = join(cdk_suite, "cdk.json")
    with open(cdk_json_path, "r") as fid:
        json_cfg = json_load(fid)

    zone = get_zone_name_and_id(zone)

    json_cfg["context"]["common"]["uuid"] = uuid
    json_cfg["context"]["common"]["ami"] = ami
    json_cfg["context"]["common"]["region"] = region
    json_cfg["context"]["route53"]["zone"]["zone_name"] = zone["name"]
    json_cfg["context"]["route53"]["zone"]["zone_id"] = zone["id"]
    json_cfg["context"]["route53"]["record"]["name"] = "www.{zone_name}".format(
        zone_name=zone["name"])

    json_cfg["context"]["route53"]["zone"]["create_new"] = False
    if create_zone:
        json_cfg["context"]["route53"]["zone"]["create_new"] = True

    with open(cdk_json_path, 'w') as fid:
        json_dump(json_cfg, fid)


def get_zone_name_and_id(zone_info: str) -> dict:
    """Convert zone info, e.g., '(mot-xxx.link, Z123abs)' to dict such as
       {
           name: mot-xxx.link
           id: Z123abs
       }

    Args:
        zone_info (str): zone information, e.g., '(mot-xxx.link, Z123abs)'

    Returns:
        dict: the zone information in a dict
    """
    zone_info = zone_info.strip("()").split(",")
    zone_name = zone_info[0].strip()
    zone_id = zone_info[1].strip()
    return {"name": zone_name, "id": zone_id}
