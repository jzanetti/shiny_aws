


from os import system
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
    else:
        raise Exception(f"job type {job} can not be performed ...")


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
    instance_id = stdout.decode("utf-8").replace("\n", "")

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

    instance_ip = stdout.decode("utf-8").replace("\n", "")

    print(f"please use {instance_ip} to access the shiny application {name} ...")

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

    instance_id = stdout.decode("utf-8").replace("\n", "")

    print(f"instance {instance_id} will be shut down ...")

    cmd = f"aws ec2 terminate-instances --instance-ids {instance_id}"

    system(cmd)
