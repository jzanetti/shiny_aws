#!/usr/bin/env python3
import os

import aws_cdk as cdk

from shiny_asg.shiny_asg_stack import ShinyAsgStack
from shiny_asg.utils import obtain_config

tags = {
    'Owner': 'Sijin',
    'Project': 'R_shiny_ASG',
    'CostCentre': 'A_M',
    'Status': 'research',
}

app = cdk.App()


config = {}
for key_name in ["common", "sg", "sns", "lb", "asg", "vpc", "route53"]:
    config[key_name] = obtain_config(app, key_name)

uuid = config["common"]["uuid"]

ShinyAsgStack(
    app, 
    f"ShinyAsgStack-{uuid}", 
    config, 
    tags=tags
)

app.synth()
