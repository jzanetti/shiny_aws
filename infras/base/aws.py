from base64 import b64encode
from json import dump as json_dump
from json import load as json_load
from os import remove, system
from os.path import basename, join
from subprocess import PIPE, Popen
from time import sleep


def check_ami(ami_name: str, overwrite_ami: bool):
    """Check if an AMI exists

    Args:
        ami_name (str): check if an AMI exists
        overwrite_ami (bool): if overwrite AMI if exists

    Raises:
        Exception: AMI exits ...
    """
    cmd = ('aws ec2 describe-images '
            '--query "Images[*].[ImageId]" '
            f'--filters "Name=name,Values={ami_name}" '
            '--output text')
    process = Popen([cmd], shell=True, stdout=PIPE)
    ami_id = process.communicate()[0]

    if len(ami_id) > 0:
        if overwrite_ami:
            ami_id = ami_id.decode("utf-8").replace("\n", "")
            cmd = f"aws ec2 deregister-image --image-id {ami_id}"
            system(cmd)
        else:
            raise Exception(f"{ami_name} exists, you may want to overwrite the AMI")
    


def get_cloud_init(cloud_init_path: str, ami_name: str) -> str:
    """Get cloud init 

    Args:
        cloud_init_path (str): Cloud init path
        ami_name (str): AMI name to be used

    Returns:
        str: decoded cloud init
    """
    cloud_init_local = "/tmp/cloud-init.sh"

    system(f"cp -rf {cloud_init_path} {cloud_init_local}")

    with open(cloud_init_local, "a") as fid:
        fid.write(f"\n\n# making AMI ...")
        fid.write(f"\nexport instance_id=`cat /var/lib/cloud/data/instance-id`")
        fid.write(f"\naws ec2 create-image --instance-id $instance_id --name {ami_name}")

    with open(cloud_init_local, "rb") as fid:
        encoded_string = b64encode(fid.read())

    decoded_string = encoded_string.decode("utf-8")

    remove(cloud_init_local)

    return decoded_string

def make_ami(cloud_init_path: str, spot_spec_path: str, ami_name: str, spot_price: float = 0.1):
    """Start a base instance

    Args:
        cloud_init_path (str): cloud init path to be used
        spot_spec_path (str): spot spec path to be used
        ami_name (str): AMI name to be used
        spot_price (float, optional): spot instance price to pay. Defaults to 0.1
    """

    decoded_string = get_cloud_init(cloud_init_path, ami_name) 

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

def shutdown_instance(expected_duration: str, query_interval_sec: int = 10):
    """Shutdown instance

    Args:
        expected_duration (str): expected duration for making AMI
    """
    stdout = ""
    while len(stdout) == 0:
        print("looking for instance ...")
        cmd = ('aws ec2 describe-instances '
            f'--filters "Name=tag:Name,Values=base_image" '
            'Name=instance-state-name,Values=running '
            '--query "Reservations[*].Instances[*].[InstanceId]" '
            '--output text')

        process = Popen([cmd], shell=True, stdout=PIPE)
        stdout = process.communicate()[0]
        sleep(query_interval_sec)

    instance_id = stdout.decode("utf-8").replace("\n", "")

    print(f"instance {instance_id} will be shut down in {expected_duration} minutes ...")

    sleep(int(expected_duration) * 60.0)

    cmd = f"aws ec2 terminate-instances --instance-ids {instance_id}"

    system(cmd)
