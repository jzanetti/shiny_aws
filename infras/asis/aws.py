from distutils.sysconfig import get_python_lib
from json import dump as json_dump
from json import load as json_load
from os import makedirs
from os.path import basename, exists, join
from shutil import copytree, rmtree

from infras.utils import (create_git_url, download_base_repository,
                          get_app_dependant_cloud_init)


def write_trigger(suite_dir: str) -> str:
    """write trigger script

    Args:
        suite_dir (str): cdk suite directory
    """
    trigger_path = join(suite_dir, "asis_trigger.sh")

    with open(trigger_path, "w") as fid:
        fid.write("#!/bin/sh")

        fid.write("\n\n# start trigger ...")
        fid.write(f"\necho 'asis trigger script ...'")
        fid.write(f"\n. $CONDA_PREFIX/../../etc/profile.d/conda.sh")
        fid.write(f"\nconda deactivate")
        fid.write(f"\nconda activate shiny_aws")
        fid.write(f"\ncd {suite_dir}")
        fid.write(f"\ncdk deploy --require-approval never")
    
    return trigger_path

def copy_asg_suite(workdir: str) -> str:
    """Copying the asg CDK suite to a working directory

    Args:
        workdir (str): working directory
    """
    if exists(workdir):
        rmtree(workdir)
    makedirs(workdir)

    src_suite = join(get_python_lib(), "infras/asis/shiny_asg")

    suite_dir = join(workdir, basename(src_suite))
    copytree(src_suite, suite_dir)

    return suite_dir



def update_cloud_init(workdir: str, cdk_suite: str, cfg: dict) -> str:
    """Creating an customized cloud-init (user data) for EC2

    Args:
        workdir (str): working directory
        cdk_suite (str): CDK suite directory
        cfg (dict): infrastructure configuration

    Returns:
        str: output cloud-init.sh
    """

    if cfg["shiny"] is not None:
        repo_url = create_git_url(cfg["shiny"])
        repo_dir = download_base_repository(workdir, repo_url)
        repo_name = basename(repo_dir)
        app_cloud_init = get_app_dependant_cloud_init(repo_dir, cfg["shiny"]["names"])

    cloud_init_path = join(cdk_suite, "cloud-init.sh")

    with open(cloud_init_path, "w") as fid:

        fid.write("#!/bin/bash")

        if cfg["shiny"] is not None:
            # clone the repository
            fid.write(f"\n\n# cloning the repository ...")
            fid.write(f"\ncd /tmp; git clone {repo_url}; "
                    f"git config --global --add safe.directory /tmp/{repo_name}; "
                    f"git checkout {cfg['shiny']['branch']}")

            # install renv
            fid.write(f"\n\n# install renv libs ...")
            for shiny_app in cfg["shiny"]["names"]:
                checkout_shiny_app = join('/tmp', repo_name, shiny_app)
                if exists(join(workdir, repo_name, shiny_app, "renv.lock")):
                    fid.write(f'\ncd {checkout_shiny_app}; Rscript -e "renv::restore();renv::isolate()"; ')

            # add shiny
            fid.write(f"\n\n# adding shiny applications ...")
            fid.write(f"\nsudo mkdir -p /srv/shiny-server/myapp")
            for shiny_app in cfg["shiny"]["names"]:
                checkout_shiny_app = join('/tmp', repo_name, shiny_app)
                fid.write(f"\nsudo cp -rf {checkout_shiny_app} /srv/shiny-server/myapp/{shiny_app}")
                fid.write(f"\nsudo chmod -R 777 /srv/shiny-server/myapp/{shiny_app}")

            # add application dependant requirements:
            fid.write(f"\n\n# adding application dependant requirements ...")
            for shiny_app in app_cloud_init:
                fid.write("\n")
                for proc_cloud_init_line in app_cloud_init[shiny_app]:
                    fid.write(proc_cloud_init_line)

            # add shiny-server:
            fid.write(f"\n\n# adding shiny-server ...")
            fid.write(f"\nsudo cp -rf /tmp/{repo_name}/shiny-server.conf /etc/shiny-server")

        # update shiny-server.conf (in case the ami is from bsis)
        fid.write(f"\nsudo sed -i '/listen 3838 127.0.0.1;/c\listen 80;' /etc/shiny-server/shiny-server.conf")
        
        # start shiny
        fid.write(f"\n\n# starting shiny ...") 
        fid.write("\nsudo service nginx stop")
        fid.write("\nsudo systemctl restart shiny-server")

def update_cdk_json(cdk_suite: str, uuid: str, cfg: dict):
    # ami: str, region: str, zone: str, create_zone: bool):
    """Update CDK json configuration

    Args:
        cdk_suite (str): cdk suite (copied from src_suite)
        uuid (str): asis unique ID
        cfg (dict): configuration
    """
    cdk_json_path = join(cdk_suite, "cdk.json")
    with open(cdk_json_path, "r") as fid:
        json_cfg = json_load(fid)

    json_cfg["context"]["common"]["uuid"] = uuid
    json_cfg["context"]["common"]["ami"] = cfg["aws"]["ami"]
    json_cfg["context"]["common"]["region"] = cfg["aws"]["region"]
    json_cfg["context"]["route53"]["zone"]["zone_name"] = cfg["aws"]["route53"]["domain_name"]
    json_cfg["context"]["route53"]["zone"]["zone_id"] = cfg["aws"]["route53"]["zone_id"]
    json_cfg["context"]["route53"]["record"]["name"] = "www.{zone_name}".format(
        zone_name=cfg["aws"]["route53"]["domain_name"])

    json_cfg["context"]["route53"]["zone"]["create_new"] = False
    if cfg["aws"]["route53"]["create_new"]:
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
