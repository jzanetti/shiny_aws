from base64 import b64encode
from json import dump as json_dump
from json import load as json_load
from os import remove, system
from os.path import basename, join
from subprocess import Popen


def get_cloud_init(cloud_init_path: str, ami_name: str, expected_baking_mins: str) -> str:
    """Get cloud init 

    Args:
        cloud_init_path (str): Cloud init path
        ami_name (str): AMI name to be used
        expected_baking_mins (str): expected baking minutes. Defaults to 30.

    Returns:
        str: decoded cloud init
    """
    cloud_init_local = "/tmp/cloud-init.sh"

    system(f"cp -rf {cloud_init_path} {cloud_init_local}")

    with open(cloud_init_local, "a") as fid:
        # add instance name
        fid.write(f"\n\n# adding instance name ...")
        fid.write(f"\nexport instance_id=`cat /var/lib/cloud/data/instance-id`")
        fid.write(f"\naws ec2 create-tags --resources $instance_id --tag Key=Name,Value='base_image'")

        # make ami
        fid.write(f"\n\n# making AMI ...")
        fid.write(f"\naws ec2 create-image --instance-id $instance_id --name {ami_name}")

        # shutdown the instance
        fid.write(f"\n\n# shutting down EC2 ...")
        fid.write(f"\nsudo shutdown -h +{expected_baking_mins} >> /tmp/shundown.log 2>&1")

    with open(cloud_init_local, "rb") as fid:
        encoded_string = b64encode(fid.read())

    decoded_string = encoded_string.decode("utf-8")

    remove(cloud_init_local)

    return decoded_string

def make_ami(cloud_init_path: str, spot_spec_path: str, ami_name: str, spot_price: float = 0.1, expected_baking_mins: str = 30):
    """Start a base instance

    Args:
        cloud_init_path (str): cloud init path to be used
        spot_spec_path (str): spot spec path to be used
        ami_name (str): AMI name to be used
        spot_price (float, optional): spot instance price to pay. Defaults to 0.1.
        expected_baking_mins (str, optional): expected baking minutes. Defaults to 30.
    """

    decoded_string = get_cloud_init(cloud_init_path, ami_name, expected_baking_mins) 

    with open(spot_spec_path) as fid:
        spot_spec = json_load(fid)

    spot_spec["UserData"] = decoded_string

    output_json = join("/tmp", basename(spot_spec_path))

    with open(output_json, 'w') as fid:
        json_dump(spot_spec, fid)

    cmd = ( "aws ec2 request-spot-instances "
            f"--spot-price {spot_price} "
            "--instance-count 1 "
            f"--launch-specification file://{output_json}")
    p = Popen([cmd], shell=True)
    p.communicate()
    remove(output_json)

