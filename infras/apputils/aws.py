


from os import system, getcwd, remove
from os.path import join, exists
from subprocess import PIPE, Popen

from infras.base.aws import check_ami


def run_utils(job: str, name: str):
    """Run shiny_aws utils

    Args:
        job (str): job name, e.g., showip or terminate
        name (str): shiny application/instance name, e.g., mot_test
    """
    if job == "terminate":
        shutdown_instance(name)
    elif job == "showip":
        show_publicip(name)
    elif job == "makeami":
        make_ami(name)
    elif job == "check":
        login_via_ip(name)
    elif job == "info":
        cloud_info(name)
    else:
        raise Exception(f"job type {job} can not be performed ...")


def cloud_info(
    name: str, 
    key_name: str = "shiny-ec2-key.pem", 
    cloud_init_tmp_file: str = "/tmp/cloud-init-output.log"):
    """Get cloud init information

    Args:
        job (str): job name, e.g., mot_dev_fleet
    """
    cwd = getcwd()
    key_path = join(cwd, key_name)

    if not exists(key_path):
        raise Exception(f"not able to find {key_path}")

    cmd = ('aws ec2 describe-instances '
           f'--filters "Name=tag:Name,Values={name}" '
           'Name=instance-state-name,Values=running '
           '--query "Reservations[*].Instances[*].PublicDnsName" '
           '--output text')

    process = Popen([cmd], shell=True, stdout=PIPE)
    stdout = process.communicate()[0]
    instance_ids = stdout.decode("utf-8").replace("\n", ",")

    instance_ids = list(filter(None, instance_ids.split(",")))

    if len(instance_ids) > 1:
        raise Exception(
            f"More than one instances named {name}, "
            "please check with your AWS admin ... ")

    instance_id = instance_ids[0]

    cmd = f"scp -i {key_path} ubuntu@{instance_id}:/var/log/cloud-init-output.log {cloud_init_tmp_file}"

    system(cmd)

    with open(cloud_init_tmp_file) as fid:
        for line in fid:
            pass
        last_line = line

    if "finished at" in last_line:
        print("cloud-init is finished ...")
    else:
        print("cloud-init is still ongoing, please wait ...")

    remove(cloud_init_tmp_file)


def login_via_ip(name: str, key_name = "shiny-ec2-key.pem"):
    """Get into an instance 

    Args:
        job (str): job name, e.g., mot_dev_fleet
        key_path (str): public key name, e.g., shiny-ec2-key.pem
    """

    cwd = getcwd()
    key_path = join(cwd, key_name)

    if not exists(key_path):
        raise Exception(f"not able to find {key_path}")

    cmd = ('aws ec2 describe-instances '
           f'--filters "Name=tag:Name,Values={name}" '
           'Name=instance-state-name,Values=running '
           '--query "Reservations[*].Instances[*].PublicDnsName" '
           '--output text')

    process = Popen([cmd], shell=True, stdout=PIPE)
    stdout = process.communicate()[0]
    instance_ids = stdout.decode("utf-8").replace("\n", ",")

    instance_ids = list(filter(None, instance_ids.split(",")))

    if len(instance_ids) > 1:
        raise Exception(
            f"More than one instances named {name}, "
            "please check with your AWS admin ... ")

    instance_id = instance_ids[0]

    cmd = f"ssh -i {key_path} ubuntu@{instance_id}"
    
    system(cmd)

def make_ami(name: str):
    """Making an AMI

    Args:
        name (str): shiny application/instance name, e.g., mot_test
    """
    cmd = ('aws ec2 describe-instances '
            f'--filters "Name=tag:Name,Values={name}" '
            'Name=instance-state-name,Values=running '
            '--query "Reservations[*].Instances[*].[InstanceId]" '
            '--output text')
    process = Popen([cmd], shell=True, stdout=PIPE)
    stdout = process.communicate()[0]
    instance_ids = stdout.decode("utf-8").replace("\n", ",")

    instance_ids = list(filter(None, instance_ids.split(",")))

    if len(instance_ids) > 1:
        raise Exception(
            f"More than one instances named {name}, "
            "please check with your AWS admin ... ")

    instance_id = instance_ids[0]

    check_ami(name, True)
    cmd = (f"\naws ec2 create-image --instance-id {instance_id} --name {name}")
    system(cmd)

    print(f"Making the AMI for {name}. "
          "please remember to shutdown the instance "
          "after making the AMI "
          "(it might take 5 - 10 minutes) ...")

def show_publicip(name: str):
    """Show the public IP address for a shiny application

    Args:
        name (str): shiny application/instance name, e.g., mot_test
    """
    cmd = ('aws ec2 describe-instances '
            f'--filters "Name=tag:Name,Values={name}" '
            'Name=instance-state-name,Values=running '
            '--query "Reservations[*].Instances[*].[PublicIpAddress]" '
            '--output text')
    process = Popen([cmd], shell=True, stdout=PIPE)
    stdout = process.communicate()[0]
    if not len(stdout):
        raise Exception(f"there is no application/instance called {name} running, "
                        "probably retry in a few minutes ? ")

    instance_ips = stdout.decode("utf-8").replace("\n", ",")

    for i, instance_ip in enumerate(instance_ips.split(",")):
        if len(instance_ip) > 0:
            print(f"({i}) please use {instance_ip} to access the shiny application {name} ...")

def shutdown_instance(name: str):
    """Shutdown instance

    Args:
        expected_duration (str): expected duration for making AMI
    """

    cmd = ('aws ec2 describe-instances '
        f'--filters "Name=tag:Name,Values={name}" '
        'Name=instance-state-name,Values=running '
        '--query "Reservations[*].Instances[*].[InstanceId]" '
        '--output text')

    process = Popen([cmd], shell=True, stdout=PIPE)
    stdout = process.communicate()[0]

    if not len(stdout):
        raise Exception(f"there is no application/instance called {name} running, "
                        "probably retry in a few minutes ? ")

    instance_ids = stdout.decode("utf-8").replace("\n", ",")

    instance_ids = list(filter(None, instance_ids.split(",")))

    if len(instance_ids) > 1:
        raise Exception(
            f"More than one instances named {name}, "
            "please shut them down from the console, "
            "or ask your AWS admin to do so")

    instance_id = instance_ids[0]

    print(f"instance {instance_id} will be shut down ...")

    cmd = f"aws ec2 terminate-instances --instance-ids {instance_id}"

    system(cmd)
