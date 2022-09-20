#!/bin/bash
# aws s3 cp s3://mot-shiny-app/r/hello_world/ /tmp/hello_world --recursive
# sudo cp -rf /tmp/hello_world/shiny-server.conf /etc/shiny-server
# sudo systemctl restart shiny-server


sudo apt-get update
sudo apt-get install docker.io docker-compose -y

aws ecr get-login-password --region ap-southeast-2 | sudo docker login --username AWS --password-stdin 839525146093.dkr.ecr.ap-southeast-2.amazonaws.com
sudo docker pull 839525146093.dkr.ecr.ap-southeast-2.amazonaws.com/shiny:hello_world

sudo docker run --rm -p 8787:8787 839525146093.dkr.ecr.ap-southeast-2.amazonaws.com/shiny:hello_world >& log &