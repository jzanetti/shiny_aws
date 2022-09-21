    
from subprocess import Popen

# -------------------------------
# instance_id: instance ID (the instance is brought up by create_base.py)
# ami_name: AMI name to be used
# -------------------------------
instance_id = "abc"
ami_name = "shiny_aws_ami"

# ----------------------------------
# Codes start from here
# ----------------------------------
cmd = f"aws ec2 create-image --instance-id {instance_id} --name {ami_name}"
p = Popen(cmd, shell=True)
p.communicate()
