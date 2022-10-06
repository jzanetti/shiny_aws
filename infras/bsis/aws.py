from base64 import b64encode
from copy import deepcopy
from json import dump as json_dump
from json import load as json_load
from os import makedirs, remove, system
from os.path import basename, exists, join
from subprocess import Popen

from infras.bsis import UNLIMITED_LIFESPAN_FLAG


def customized_userdata(workdir: str, cfg: dict, lifespan: str) -> str:
    """Creating an customized cloud-init (user data) for EC2

    Args:
        workdir (str): working directory
        cfg (dict): infrastructure configuration
        lifespan (str): server life span in minutes (or unlimited)

    Returns:
        str: output cloud-init.sh
    """
    src_path = join(
        cfg["shiny"]["s3"], 
        cfg["shiny"]["name"], 
        cfg["shiny"]["userdata"]
    )
    dest_path = join(workdir, "cloud-init.sh")

    system(f"aws s3 cp {src_path} {dest_path}")

    with open(dest_path, "a") as fid:

        shiny_name = cfg["shiny"]["name"]
        fid.write(f"\nexport instance_id=`cat /var/lib/cloud/data/instance-id`")
        fid.write(f"\naws ec2 create-tags --resources $instance_id --tag Key=Name,Value='{shiny_name}'")

        if cfg["user"]["authentication"]:
            fid.write("\nsudo service nginx stop")
            fid.write("\nsudo systemctl stop shiny-server")
            fid.write("\nsudo sed -i '/listen 80;/c\listen 3838 127.0.0.1;' /etc/shiny-server/shiny-server.conf")
            fid.write("\nsudo systemctl start shiny-server")
            fid.write("\nsudo service nginx start")
        else:
            fid.write("\nsudo service nginx stop")
            fid.write("\nsudo systemctl restart shiny-server")

        if cfg["user"]["elastic_ip"] is not None:
            fid.write(f"\nsudo aws ec2 associate-address --instance-id $instance_id --allocation-id {cfg['user']['elastic_ip']}")
        
        if lifespan != UNLIMITED_LIFESPAN_FLAG: # lifespan is noted as minutes
            lifespan = int(lifespan)
            fid.write(f"\nsudo shutdown -h +{lifespan} >> /tmp/shundown.log 2>&1")

    return dest_path


def create_userdata(workdir: str, cfg: dict, lifespan: str) -> str:
    """Convert cloud-init.sh to base64, and attach the instance lifespan
        if it is not production run

    Args:
        workdir (str): working directory
        cfg (str): infrastructure configuration
        lifespan (str): server lifespan in minutes (or unlimited)

    Returns:
        str: configuration base64 string
    """
    cloud_init_path = customized_userdata(workdir, cfg, lifespan)

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


def create_infras(workdir: str, cfg: dict, lifespan: str) -> str:
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
    user_data = create_userdata(workdir, cfg, lifespan)

    output_json = update_spot_spec(workdir, user_data, spot_spec_path)

    cmd = ( "aws ec2 request-spot-instances "
            f"--spot-price {cfg['user']['spot_price']} "
            "--instance-count 1 "
            f"--launch-specification file://{output_json}")
    print(cmd)
    p = Popen([cmd], shell=True)
    p.communicate()
