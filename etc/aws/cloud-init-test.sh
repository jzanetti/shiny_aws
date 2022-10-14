#!/bin/bash

sudo apt-get update
sudo apt install unzip

# install awscli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# create tag
export instance_id=`cat /var/lib/cloud/data/instance-id`
sudo aws ec2 create-tags --resources $instance_id --tag Key=Name,Value='base_image'

