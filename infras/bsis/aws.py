from base64 import b64encode
from copy import deepcopy
from json import dump as json_dump
from json import load as json_load
from os import makedirs
from os.path import basename, exists, join
from subprocess import Popen

from infras.bsis import UNLIMITED_LIFESPAN_FLAG
from infras.utils import (create_git_url, download_base_repository,
                          get_app_dependant_cloud_init, obtain_private_packages)
from infras import SHINYAPP_LOC

def customized_userdata(workdir: str, cfg: dict, lifespan: str, cfg_name: str) -> str:
    """Creating an customized cloud-init (user data) for EC2

    Args:
        workdir (str): working directory
        cfg (dict): infrastructure configuration
        lifespan (str): server life span in minutes (or unlimited)

    Returns:
        str: output cloud-init.sh
    """

    if cfg["shiny"] is not None:
        repo_url = create_git_url(cfg["shiny"])
        repo_dir = download_base_repository(workdir, repo_url, cfg['shiny']['branch'])
        repo_name = basename(repo_dir)
        app_cloud_init = get_app_dependant_cloud_init(repo_dir, cfg["shiny"]["names"])

    cloud_init_path = join(workdir, "cloud-init.sh")

    with open(cloud_init_path, "w") as fid:

        fid.write("#!/bin/bash")

        # add instance name
        fid.write(f"\n\n# adding instance name ...")
        fid.write(f"\nexport instance_id=`cat /var/lib/cloud/data/instance-id`")
        fid.write(f"\naws ec2 create-tags --resources $instance_id --tag Key=Name,Value='{cfg_name}'")

        # add elastic_ip
        if cfg["user"]["elastic_ip"] is not None:
            fid.write(f"\n\n# adding elastic IP ...")
            fid.write(f"\nsudo aws ec2 associate-address --instance-id $instance_id --allocation-id {cfg['user']['elastic_ip']}")
        
        # add lifespan
        if lifespan != UNLIMITED_LIFESPAN_FLAG: # lifespan is noted as minutes
            lifespan = int(lifespan)
            fid.write(f"\n\n# adding life span ...")
            fid.write(f"\nsudo shutdown -h +{lifespan} >> /tmp/shundown.log 2>&1")

        if cfg["shiny"] is not None:
            # clone the repository
            fid.write(f"\n\n# cloning the repository ...")
            fid.write(f"\ncd /tmp; git clone {repo_url}; "
                    f"git config --global --add safe.directory /tmp/{repo_name}; "
                    f"cd /tmp/{repo_name}; git checkout {cfg['shiny']['branch']}")

            # add shiny
            fid.write(f"\n\n# adding shiny applications ...")
            for shiny_app in cfg["shiny"]["names"]:

                shiny_app_name = cfg["shiny"]["names"][shiny_app]
                checkout_shiny_app = join('/tmp', repo_name, shiny_app)

                fid.write(f"\nsudo rm -rf {SHINYAPP_LOC}/{shiny_app_name}")
                fid.write(f"\nsudo mkdir -p {SHINYAPP_LOC}/{shiny_app_name}")
                fid.write(f"\nsudo cp -rf {checkout_shiny_app}/* {SHINYAPP_LOC}/{shiny_app_name}")
                fid.write(f"\nsudo chmod -R 777 {SHINYAPP_LOC}/{shiny_app_name}")

            # add application dependant requirements:
            fid.write(f"\n\n# adding application dependant requirements ...")
            for shiny_app in app_cloud_init:
                
                shiny_app_name = cfg["shiny"]["names"][shiny_app]

                fid.write("\n")
                for proc_cloud_init_line in app_cloud_init[shiny_app]:
                    if not proc_cloud_init_line.startswith("#"):
                        fid.write(f"cd {SHINYAPP_LOC}/{shiny_app_name}; {proc_cloud_init_line}")

            # install renv
            # note that renv::repair is needed if we migrate renv from one OS to another
            # otherwise the error will be
            #   "The following package(s) have broken symlinks into the cache"
            # see details: https://github.com/rstudio/renv/issues/378
            fid.write(f"\n\n# install renv libs ...")
            fid.write(f'\nsudo R -e "install.packages(\'renv\')"')
            for shiny_app in cfg["shiny"]["names"]:

                shiny_app_name = cfg["shiny"]["names"][shiny_app]

                shiny_app_path = join(SHINYAPP_LOC, shiny_app_name)
                renv_lock_file = join(workdir, repo_name, shiny_app, "renv.lock")
                if exists(renv_lock_file):
                    private_pkgs = obtain_private_packages(renv_lock_file)

                    if private_pkgs is None:
                        restore_cmd = f"renv::restore(project='{shiny_app_path}')"
                    else:
                        restore_cmd = f"renv::restore(project='{shiny_app_path}', exclude={private_pkgs})"

                    fid.write(f'\ncd {shiny_app_path}; sudo Rscript -e "{restore_cmd};renv::repair();renv::isolate()"')

            # add shiny-server:
            fid.write(f"\n\n# adding shiny-server ...")
            fid.write(f"\nsudo cp -rf /tmp/{repo_name}/shiny-server.conf /etc/shiny-server")

        # add authentication and start shiny
        fid.write(f"\n\n# adding authentication and starting shiny ...")
        if cfg["user"]["authentication"]:
            fid.write("\nsudo service nginx stop")
            fid.write("\nsudo systemctl stop shiny-server")
            fid.write("\nsudo sed -i '/listen 80;/c\listen 3838 127.0.0.1;' /etc/shiny-server/shiny-server.conf")
            fid.write("\nsudo systemctl start shiny-server")
            fid.write("\nsudo service nginx start")
        else:
            fid.write("\nsudo service nginx stop")
            fid.write("\nsudo systemctl restart shiny-server")
    
    return cloud_init_path


def create_userdata(workdir: str, cfg: dict, lifespan: str, cfg_name: str) -> str:
    """Convert cloud-init.sh to base64, and attach the instance lifespan
        if it is not production run

    Args:
        workdir (str): working directory
        cfg (str): infrastructure configuration
        lifespan (str): server lifespan in minutes (or unlimited)

    Returns:
        str: configuration base64 string
    """
    cloud_init_path = customized_userdata(workdir, cfg, lifespan, cfg_name)

    with open(cloud_init_path, "rb") as fid:
        encoded_string = b64encode(fid.read())
    return encoded_string.decode("utf-8") 


def update_spot_spec(workdir: str, base64_init: str, spot_spec_path: str) -> str:
    """Update spot spec file (json) based on the cloud-init

    Args:
        workdir (str): working directory
        base64_init (str): base64 encoded cloud-init.sh
        spot_spec_path (str, optional): the path for spot specification. Defaults to "spot_spec.json".
    """
    with open(spot_spec_path) as fid:
        spot_spec = json_load(fid)
  
    spot_spec["UserData"] = base64_init

    output_json = join(workdir, basename(spot_spec_path))

    with open(output_json, 'w') as fid:
        json_dump(spot_spec, fid)

    return output_json


def write_base_spot_spec(workdir: str, cfg: dict) -> str:
    """Write base spot spec file

    Args:
        workdir (str): working directory
        cfg (dict): infras configuration

    Returns:
        str: written spot spec file
    """
    spot_spec = deepcopy(cfg["aws"])

    base_spot_spec_file = join(workdir, "base_spot_spec.json")
    with open(base_spot_spec_file, 'w') as fid:
        json_dump(spot_spec, fid)

    return base_spot_spec_file


def create_infras(workdir: str, cfg: dict, lifespan: str, cfg_name: str) -> str:
    """Bring up an instance to host shiny application

    Args:
        workdir (str): working directory
        cfg (str): infrastructure configuration file
        lifespan (str): lifespan in minutes (or unlimited)

    Returns:
        str: the instance information
    """

    if not exists(workdir):
        makedirs(workdir)

    spot_spec_path = write_base_spot_spec(workdir, cfg)
    user_data = create_userdata(workdir, cfg, lifespan, cfg_name)

    output_json = update_spot_spec(workdir, user_data, spot_spec_path)

    cmd = ( "aws ec2 request-spot-instances "
            f"--spot-price {cfg['user']['spot_price']} "
            "--instance-count 1 "
            f"--launch-specification file://{output_json}")
    print(cmd)
    p = Popen([cmd], shell=True)
    p.communicate()
